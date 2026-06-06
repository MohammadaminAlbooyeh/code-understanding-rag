import { useState } from 'react';
import { documentationAPI } from '../services/documentation_api';

export function useDocumentation() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const generate = async (codeId, type) => {
    setLoading(true);
    try {
      const result = await documentationAPI.generate(codeId, type);
      setData(result);
      return result;
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { generate, data, loading, error };
}
