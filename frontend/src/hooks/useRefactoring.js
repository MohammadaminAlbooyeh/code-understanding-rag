import { useState } from 'react';

export function useRefactoring() {
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [error, setError] = useState(null);

  const getSuggestions = async (codeId) => {
    setLoading(true);
    try {
      setSuggestions([]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { getSuggestions, suggestions, loading, error };
}
