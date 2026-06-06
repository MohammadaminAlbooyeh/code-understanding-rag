import React from 'react';
import { useParams } from 'react-router-dom';
import RefactoringCard from '../components/RefactoringCard';

function RefactoringPage() {
  const { id } = useParams();
  return (
    <div className="refactoring-page">
      <h1>Refactoring Suggestions</h1>
      <RefactoringCard codeId={id} />
    </div>
  );
}

export default RefactoringPage;
