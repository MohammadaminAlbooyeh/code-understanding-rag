import { useState } from 'react';
import { analysisAPI } from '../services/analysis_api';

export function useAnalysis() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const methods = {
    parse: analysisAPI.parse,
    complexity: analysisAPI.complexity,
    bugs: analysisAPI.bugs,
    security: analysisAPI.security,
  };

  const analyze = async (codeId, type) => {
    setLoading(true);
    try {
      const method = methods[type];
      if (!method) {
        throw new Error(`Unknown analysis type: ${type}`);
      }
      const result = await method(codeId);
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
