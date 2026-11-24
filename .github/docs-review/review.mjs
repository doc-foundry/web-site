// Reviews changed Markdown lines against style-guide.md with Claude, then posts the findings as
// one pull request review. Run locally with --dry-run to print findings instead:
//   node .github/docs-review/review.mjs --dry-run site/blog/some-post.md
import Anthropic from "@anthropic-ai/sdk";
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const MODEL = process.env.DOCS_REVIEW_MODEL ?? "claude-opus-5-5";
const MAX_FILES = 20;
const MAX_CHARS = 60_000; // about 15k tokens; larger files are skipped, not truncated

const FINDINGS_SCHEMA = {
  type: "object",
  properties: {
    findings: {
      type: "array",
      items: {
        type: "object",
        properties: {
          line: { type: "integer" },
          rule: { type: "string" },
          problem: { type: "string" },
          replacement: { type: "string" },
        },
        required: ["line", "rule", "problem", "replacement"],
        additionalProperties: false,
      },
    },
  },
  required: ["findings"],
  additionalProperties: false,
};

const SYSTEM = `You review documentation changes for a docs-as-code site. Apply the house style
below to the changed lines only; read the rest of the file for context.

Report a finding only when a rule is clearly broken and a reader would notice. Silence is a valid
result. Never flag vivid phrasing for being vivid (rule 6), and don't report what a spelling or
terminology linter already catches.

For each finding give:
- line: the line number, which must be one of the changed lines
- rule: the rule number and short name, for example "2 Concise"
- problem: one sentence on what's wrong and why it matters to the reader
- replacement: the full corrected text of that one line, or "" when the fix spans several lines

${readFileSync(path.join(here, "style-guide.md"), "utf8")}`;

function git(...args) {
  return execFileSync("git", args, { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 });
}

// Maps each file to the set of line numbers added or changed between two commits.
function addedLines(base, head) {
  const diff = git("diff", "--unified=0", "--diff-filter=AM", base, head, "--", "*.md", "*.mdx");
  const files = new Map();
  let current = null;
  for (const row of diff.split("\n")) {
    if (row.startsWith("+++ ")) {
      current = row === "+++ /dev/null" ? null : row.slice("+++ b/".length);
      if (current) files.set(current, new Set());
      continue;
    }
    const hunk = current && /^@@ -\S+ \+(\d+)(?:,(\d+))? @@/.exec(row);
    if (hunk) {
      const start = Number(hunk[1]);
      const count = hunk[2] === undefined ? 1 : Number(hunk[2]);
      for (let n = start; n < start + count; n++) files.get(current).add(n);
    }
  }
  return files;
}

function commitExists(sha) {
  try {
    git("cat-file", "-e", `${sha}^{commit}`);
    return true;
  } catch {
    return false;
  }
}

// On a new push, review only what that push changed, so earlier findings aren't posted twice.
// Lines must also be in the PR diff, or GitHub rejects the comment.
function linesToReview() {
  const { BASE_SHA, HEAD_SHA, BEFORE_SHA } = process.env;
  const prLines = addedLines(BASE_SHA, HEAD_SHA);
  if (!BEFORE_SHA || /^0+$/.test(BEFORE_SHA) || !commitExists(BEFORE_SHA)) return prLines;
  const pushLines = addedLines(BEFORE_SHA, HEAD_SHA);
  const result = new Map();
  for (const [file, lines] of pushLines) {
    const inPr = prLines.get(file);
    if (!inPr) continue;
    const both = new Set([...lines].filter((n) => inPr.has(n)));
    if (both.size) result.set(file, both);
  }
  return result;
}

function channel(file) {
  return file.startsWith("site/blog/") ? "blog post (rules 1–11)" : "docs page (rules 1–6, 8, 10)";
}

async function reviewFile(client, file, changed) {
  const text = readFileSync(file, "utf8");
  if (text.length > MAX_CHARS) {
    console.warn(`Skipped ${file}: ${text.length} characters is over the ${MAX_CHARS} limit.`);
    return [];
  }
  const numbered = text
    .split("\n")
    .map((row, i) => `${String(i + 1).padStart(4)}| ${row}`)
    .join("\n");
  const changedList = [...changed].sort((a, b) => a - b).join(", ");

  const response = await client.beta.messages.create({
    model: MODEL,
    max_tokens: 16000,
    betas: ["server-side-fallback-2026-07-01"],
    fallbacks: "default",
    system: SYSTEM,
    output_config: {
      effort: "medium",
      format: { type: "json_schema", schema: FINDINGS_SCHEMA },
    },
    messages: [
      {
        role: "user",
        content: `File: ${file}\nType: ${channel(file)}\nChanged lines: ${changedList}\n\n${numbered}`,
      },
    ],
  });

  if (response.stop_reason !== "end_turn") {
    console.warn(`Skipped ${file}: the model stopped with "${response.stop_reason}".`);
    return [];
  }
  const block = response.content.find((b) => b.type === "text");
  const { findings } = JSON.parse(block.text);
  const { input_tokens, output_tokens } = response.usage;
  console.log(`${file}: ${findings.length} finding(s), ${input_tokens} in / ${output_tokens} out`);
  // The model may cite an unchanged line; GitHub would reject a comment there.
  return findings.filter((f) => changed.has(f.line)).map((f) => ({ ...f, file }));
}

function commentBody(f) {
  const lines = [`**${f.rule}.** ${f.problem}`];
  if (f.replacement) lines.push("", "```suggestion", f.replacement, "```");
  return lines.join("\n");
}

async function postReview(findings) {
  const { GITHUB_TOKEN, GITHUB_REPOSITORY, PR_NUMBER, HEAD_SHA } = process.env;
  const body = findings.length
    ? `Style review: ${findings.length} finding(s). Advisory only; resolve or dismiss as you see fit.`
    : "Style review: no findings on the changed lines.";
  const res = await fetch(
    `https://api.github.com/repos/${GITHUB_REPOSITORY}/pulls/${PR_NUMBER}/reviews`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${GITHUB_TOKEN}`,
        Accept: "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
      },
      body: JSON.stringify({
        commit_id: HEAD_SHA,
        event: "COMMENT",
        body,
        comments: findings.map((f) => ({
          path: f.file,
          line: f.line,
          side: "RIGHT",
          body: commentBody(f),
        })),
      }),
    },
  );
  if (!res.ok) throw new Error(`GitHub review failed: ${res.status} ${await res.text()}`);
}

async function main() {
  const args = process.argv.slice(2);
  const dryRun = args[0] === "--dry-run";

  let targets;
  if (dryRun) {
    // Local run: treat every line of the named files as changed.
    targets = new Map(
      args.slice(1).filter(existsSync).map((file) => {
        const count = readFileSync(file, "utf8").split("\n").length;
        return [file, new Set(Array.from({ length: count }, (_, i) => i + 1))];
      }),
    );
  } else {
    targets = linesToReview();
  }

  const files = [...targets.keys()].slice(0, MAX_FILES);
  if (targets.size > MAX_FILES) {
    console.warn(`Reviewing the first ${MAX_FILES} of ${targets.size} changed files.`);
  }
  if (!files.length) {
    console.log("No changed Markdown lines to review.");
    return;
  }

  const client = new Anthropic();
  const results = await Promise.all(files.map((f) => reviewFile(client, f, targets.get(f))));
  const findings = results.flat();

  if (dryRun) {
    for (const f of findings) {
      console.log(`\n${f.file}:${f.line}  [${f.rule}]\n  ${f.problem}`);
      if (f.replacement) console.log(`  → ${f.replacement}`);
    }
    return;
  }
  await postReview(findings);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
