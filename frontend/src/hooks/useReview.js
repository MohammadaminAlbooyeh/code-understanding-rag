import { useState } from 'react';
import { reviewAPI } from '../services/review_api';

export function useReview() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const review = async (codeId) => {
    setLoading(true);
    try {
      const result = await reviewAPI.review(codeId);
      setData(result);
      return result;
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { review, data, loading, error };
}
