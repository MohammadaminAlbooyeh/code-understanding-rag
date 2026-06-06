import React from 'react';
import { useParams } from 'react-router-dom';
import ReviewCard from '../components/ReviewCard';

function ReviewPage() {
  const { id } = useParams();
  return (
    <div className="review-page">
      <h1>Code Review</h1>
      <ReviewCard reviewId={id} />
    </div>
  );
}

export default ReviewPage;
