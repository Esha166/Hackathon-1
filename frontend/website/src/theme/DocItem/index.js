/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import useWindowSize from '@theme/hooks/useWindowSize';
import DocPaginator from '@theme/DocPaginator';
import DocVersionBanner from '@theme/DocVersionBanner';
import Seo from '@theme/Seo';
import DocItemFooter from '@theme/DocItemFooter';
import TOC from '@theme/TOC';
import TOCCollapsible from '@theme/TOCCollapsible';
import {MainHeading} from '@theme/Heading';
import styles from './styles.module.css';
import {ThemeClassNames} from '@docusaurus/theme-common';
import PersonalizeButton from '../../../src/components/Chapter/PersonalizeButton'; // Import PersonalizeButton

export default function DocItem(props) {
  const {content: DocContent, versionMetadata} = props;
  const {metadata, frontMatter} = DocContent;
  const {
    image,
    keywords,
    hide_title: hideTitle,
    hide_table_of_contents: hideTableOfContents,
  } = frontMatter;
  const {description, title} = metadata; 

  const [originalChapterContent, setOriginalChapterContent] = useState('');
  const [displayChapterContent, setDisplayChapterContent] = useState<string | React.ElementType>('');

  // Extract chapter ID from metadata (e.g., id or slug)
  const chapterId = metadata.id || metadata.slug || title;

  useEffect(() => {
    // When the component mounts or metadata changes, capture the original content
    // DocContent is a React component, so we need to render it to get its output
    // This is a simplified approach, a more robust solution might involve:
    // 1. Fetching the raw markdown content of the current page.
    // 2. Storing it in state.
    // For now, we'll use a placeholder for the content passed to the PersonalizeButton.
    // The actual chapter content will be fetched on demand by the backend based on chapter_id.
    setOriginalChapterContent(null); // Clear previous content
    setDisplayChapterContent(<DocContent />); // Render original component by default
  }, [DocContent]);

  const handlePersonalizeCallback = (personalizedContent: string) => {
    // When personalized content is received, update the display
    setDisplayChapterContent(personalizedContent);
  };

  const handleResetPersonalization = () => {
    setDisplayChapterContent(<DocContent />);
    // Optionally, clear any personalized content state here
  }


  // We only add a title if:
  // - user asks to hide it with frontmatter
  // - the markdown content does not already contain a top-level h1 heading
  const shouldAddTitle =
    !hideTitle && typeof DocContent.contentTitle === 'undefined';
  const windowSize = useWindowSize();
  const canRenderTOC =
    !hideTableOfContents && DocContent.toc && DocContent.toc.length > 0;
  const renderTocDesktop =
    canRenderTOC && (windowSize === 'desktop' || windowSize === 'ssr');
  return (
    <>
      <Seo
        {...{
          title,
          description,
          keywords,
          image,
        }}
      />

      <div className="row">
        <div
          className={clsx('col', {
            [styles.docItemCol]: !hideTableOfContents,
          })}>
          <DocVersionBanner versionMetadata={versionMetadata} />
          <div className={styles.docItemContainer}>
            <article>
              {versionMetadata.badge && (
                <span
                  className={clsx(
                    ThemeClassNames.docs.docVersionBadge,
                    'badge badge--secondary',
                  )}>
                  Version: {versionMetadata.label}
                </span>
              )}

              {canRenderTOC && (
                <TOCCollapsible
                  toc={DocContent.toc}
                  className={clsx(
                    ThemeClassNames.docs.docTocMobile,
                    styles.tocMobile,
                  )}
                />
              )}

              {/* Personalize Button Injection */}
              {chapterId && (
                <PersonalizeButton chapterId={chapterId} onPersonalize={handlePersonalizeCallback} />
              )}
              {displayChapterContent !== DocContent && (
                <button onClick={handleResetPersonalization} style={{marginTop: '10px'}}>
                  Show Original Content
                </button>
              )}


              <div
                className={clsx(ThemeClassNames.docs.docMarkdown, 'markdown')}>
                {/*
                Title can be declared inside md content or declared through frontmatter and added manually
                To make both cases consistent, the added title is added under the same div.markdown block
                See https://github.com/facebook/docusaurus/pull/4882#issuecomment-853021120
                */}
                {shouldAddTitle && <MainHeading>{title}</MainHeading>}

                {/* Render dynamic content */}
                {typeof displayChapterContent === 'string' ? (
                  <div dangerouslySetInnerHTML={{ __html: displayChapterContent }} />
                ) : (
                  displayChapterContent
                )}
              </div>

              <DocItemFooter {...props} />
            </article>

            <DocPaginator metadata={metadata} />
          </div>
        </div>
        {renderTocDesktop && (
          <div className="col col--3">
            <TOC
              toc={DocContent.toc}
              className={ThemeClassNames.docs.docTocDesktop}
            />
          </div>
        )}
      </div>
    </>
  );
}