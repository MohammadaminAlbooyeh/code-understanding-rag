import React from 'react';
import { NavLink } from 'react-router-dom';

function Sidebar() {
  return (
    <aside className="sidebar">
      <nav className="sidebar-nav">
        <NavLink to="/">Dashboard</NavLink>
        <NavLink to="/upload">Upload Code</NavLink>
        <NavLink to="/history">History</NavLink>
        <NavLink to="/dependencies">Dependencies</NavLink>
      </nav>
    </aside>
  );
}

export default Sidebar;
