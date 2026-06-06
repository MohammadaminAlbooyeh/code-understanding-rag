import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div className="home-page">
      <h1>Code Understanding RAG</h1>
      <p>Analyze, understand, and document your code with AI-powered RAG system.</p>
      <div className="home-features">
        <div className="feature">
          <h3><Link to="/upload">Upload Code</Link></h3>
          <p>Upload source code files for analysis</p>
        </div>
        <div className="feature">
          <h3><Link to="/analyze">Analyze</Link></h3>
          <p>Run complexity, bug, and security analysis</p>
        </div>
        <div className="feature">
          <h3><Link to="/qa">Ask Questions</Link></h3>
          <p>Ask questions about your codebase</p>
        </div>
        <div className="feature">
          <h3><Link to="/docs">Documentation</Link></h3>
          <p>Generate and view code documentation</p>
        </div>
        <div className="feature">
          <h3><Link to="/review">Code Review</Link></h3>
          <p>Get AI-powered code review suggestions</p>
        </div>
        <div className="feature">
          <h3><Link to="/history">History</Link></h3>
          <p>View your analysis history</p>
        </div>
      </div>
    </div>
  );
}

export default HomePage;
