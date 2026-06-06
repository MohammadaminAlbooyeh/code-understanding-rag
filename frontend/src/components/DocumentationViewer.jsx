import React from 'react';
import ReactMarkdown from 'react-markdown';

function DocumentationViewer({ docId }) {
  return (
    <div className="documentation-viewer">
      <ReactMarkdown># Documentation</ReactMarkdown>
    </div>
  );
}

export default DocumentationViewer;
