import React, { useState, useEffect } from 'react';
import { codeAPI } from '../services/code_api';

function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    codeAPI.list()
      .then((res) => setHistory(res.data || res || []))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="history-page">
      <h1>Analysis History</h1>
      {loading && <p>Loading history...</p>}
      {error && <p className="error">{error}</p>}
      {!loading && !error && history.length === 0 && <p>No analysis history found.</p>}
      <ul>
        {history.map((item, i) => (
          <li key={item.id || i}>
            {item.filename || item.name || `Item ${i + 1}`}
            {item.created_at && <span className="date"> — {new Date(item.created_at).toLocaleString()}</span>}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default HistoryPage;
