import { useState } from 'react';
import { qaAPI } from '../services/qa_api';

export function useQA() {
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState(null);
  const [error, setError] = useState(null);

  const ask = async (codeId, question) => {
    setLoading(true);
    try {
      const result = await qaAPI.ask(codeId, question);
      setAnswer(result);
      return result;
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { ask, answer, loading, error };
}
