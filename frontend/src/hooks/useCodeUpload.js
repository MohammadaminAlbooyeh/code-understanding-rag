import { useState } from 'react';
import { codeAPI } from '../services/code_api';

export function useCodeUpload() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const upload = async (file) => {
    setLoading(true);
    try {
      const result = await codeAPI.upload(file);
      return result;
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { upload, loading, error };
}
