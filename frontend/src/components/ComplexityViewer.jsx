import React from 'react';

function ComplexityViewer({ complexity }) {
  return (
    <div className="complexity-viewer">
      <h3>Complexity Analysis</h3>
      <pre>{JSON.stringify(complexity, null, 2)}</pre>
    </div>
  );
}

export default ComplexityViewer;
