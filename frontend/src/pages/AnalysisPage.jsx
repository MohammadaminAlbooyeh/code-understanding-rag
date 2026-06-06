import React from 'react';
import { useParams } from 'react-router-dom';
import AnalysisCard from '../components/AnalysisCard';

function AnalysisPage() {
  const { id } = useParams();
  return (
    <div className="analysis-page">
      <h1>Code Analysis</h1>
      <AnalysisCard analysisId={id} />
    </div>
  );
}

export default AnalysisPage;
