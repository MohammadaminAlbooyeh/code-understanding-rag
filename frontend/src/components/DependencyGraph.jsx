import React from 'react';

function DependencyGraph() {
  return (
    <div className="dependency-graph">
      <h3>Dependency Graph</h3>
      <p>Visual dependency graph will be rendered here using D3.js.</p>
      <div className="graph-placeholder" style={{
        width: '100%',
        height: '400px',
        border: '1px dashed #ccc',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: '#999',
      }}>
        Graph visualization area
      </div>
    </div>
  );
}

export default DependencyGraph;
