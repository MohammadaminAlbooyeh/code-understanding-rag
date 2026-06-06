import React, { useState, useEffect } from 'react';
import { reviewAPI } from '../services/review_api';

function ReviewCard({ reviewId }) {
  const [review, setReview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!reviewId) return;
    setLoading(true);
    reviewAPI.get(reviewId)
      .then((res) => setReview(res.data || res))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [reviewId]);

  if (!reviewId) return <div className="review-card"><p>No review selected.</p></div>;
  if (loading) return <div className="review-card"><p>Loading review...</p></div>;
  if (error) return <div className="review-card"><p className="error">{error}</p></div>;

  const score = review.quality_score ?? review.score ?? 'N/A';
  const issues = review.issues || [];
  const suggestions = review.suggestions || [];

  return (
    <div className="review-card">
      <h3>Code Review</h3>
      <p><strong>Quality Score:</strong> {score}</p>
      {issues.length > 0 && (
        <>
          <h4>Issues ({issues.length})</h4>
          <ul>
            {issues.map((issue, i) => (
              <li key={i}>{issue.message || issue}</li>
            ))}
          </ul>
        </>
      )}
      {suggestions.length > 0 && (
        <>
          <h4>Suggestions</h4>
          <ul>
            {suggestions.map((s, i) => (
              <li key={i}>{s.message || s}</li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default ReviewCard;
