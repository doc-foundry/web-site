import type {ReactNode} from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout description={siteConfig.tagline}>
      <main className={styles.placeholder}>
        <Heading as="h1">{siteConfig.title}</Heading>
        <p>{siteConfig.tagline}</p>
        <p>Site under construction.</p>
      </main>
    </Layout>
  );
}
