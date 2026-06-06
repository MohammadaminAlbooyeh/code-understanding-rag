import React, { useState, useEffect } from 'react';
import { analysisAPI } from '../services/analysis_api';

function AnalysisCard({ analysisId }) {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!analysisId) return;
    setLoading(true);
    analysisAPI.get(analysisId)
      .then((res) => setAnalysis(res.data || res))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [analysisId]);

  if (!analysisId) return <div className="analysis-card"><p>No analysis selected.</p></div>;
  if (loading) return <div className="analysis-card"><p>Loading analysis...</p></div>;
  if (error) return <div className="analysis-card"><p className="error">{error}</p></div>;

  return (
    <div className="analysis-card">
      <h3>Analysis Results</h3>
      <pre>{JSON.stringify(analysis, null, 2)}</pre>
    </div>
  );
}

export default AnalysisCard;
