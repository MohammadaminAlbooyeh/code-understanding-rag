import { useState } from 'react';
import { reviewAPI } from '../services/review_api';

export function useRefactoring() {
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [error, setError] = useState(null);

  const getSuggestions = async (codeId) => {
    setLoading(true);
    try {
      const result = await reviewAPI.refactor(codeId);
      setSuggestions(result);
      return result;
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { getSuggestions, suggestions, loading, error };
}
