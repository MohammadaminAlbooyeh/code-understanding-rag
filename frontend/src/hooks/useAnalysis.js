import { useState } from 'react';
import { analysisAPI } from '../services/analysis_api';

export function useAnalysis() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const analyze = async (codeId, type) => {
    setLoading(true);
    try {
      const result = await analysisAPI.analyze(codeId, type);
      setData(result);
      return result;
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { analyze, data, loading, error };
}
