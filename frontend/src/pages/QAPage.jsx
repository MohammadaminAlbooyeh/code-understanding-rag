import React from 'react';
import { useParams } from 'react-router-dom';
import QABox from '../components/QABox';

function QAPage() {
  const { id } = useParams();
  return (
    <div className="qa-page">
      <h1>Ask Questions</h1>
      <QABox codeId={id} />
    </div>
  );
}

export default QAPage;
