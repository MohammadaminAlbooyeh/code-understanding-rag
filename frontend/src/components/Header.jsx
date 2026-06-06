import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="header">
      <Link to="/" className="header-logo">Code RAG</Link>
      <nav className="header-nav">
        <Link to="/upload">Upload</Link>
        <Link to="/history">History</Link>
        <Link to="/dependencies">Dependencies</Link>
      </nav>
    </header>
  );
}

export default Header;
