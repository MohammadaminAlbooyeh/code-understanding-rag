import React from 'react';
import DependencyGraph from '../components/DependencyGraph';

function DependencyPage() {
  return (
    <div className="dependency-page">
      <h1>Dependencies</h1>
      <DependencyGraph />
    </div>
  );
}

export default DependencyPage;
