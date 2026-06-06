import { useState, useCallback } from 'react';
import api from '../services/api';

export function useAPI(endpoint) {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const get = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.get(endpoint);
      setData(res.data);
      return res.data;
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [endpoint]);

  const post = useCallback(async (body) => {
    setLoading(true);
    try {
      const res = await api.post(endpoint, body);
      setData(res.data);
      return res.data;
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [endpoint]);

  return { get, post, data, loading, error };
}
