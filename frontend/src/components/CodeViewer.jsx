import React from 'react';

function CodeViewer({ code, language }) {
  return (
    <pre className="code-viewer">
      <code>{code}</code>
    </pre>
  );
}

export default CodeViewer;
