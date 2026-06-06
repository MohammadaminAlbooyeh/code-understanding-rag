import React from 'react';

function ErrorDisplay({ message, onRetry }) {
  return (
    <div className="error-display">
      <p>Error: {message}</p>
      {onRetry && <button onClick={onRetry}>Retry</button>}
    </div>
  );
}

export default ErrorDisplay;
