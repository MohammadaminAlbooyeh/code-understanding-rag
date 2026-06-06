import React from 'react';

function BugCard({ bugs }) {
  return (
    <div className="bug-card">
      <h3>Detected Bugs</h3>
      {bugs?.map((bug, i) => (
        <div key={i} className="bug-item">{bug.message}</div>
      ))}
    </div>
  );
}

export default BugCard;
