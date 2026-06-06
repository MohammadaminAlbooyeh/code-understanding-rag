import React, { useState } from 'react';
import { useQA } from '../hooks/useQA';

function QABox({ codeId }) {
  const [question, setQuestion] = useState('');
  const { ask, answer, loading, error } = useQA();

  const handleAsk = async () => {
    if (!question.trim() || !codeId) return;
    await ask(codeId, question);
  };

  return (
    <div className="qa-box">
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question about your code..."
      />
      <button onClick={handleAsk} disabled={loading || !question.trim()}>
        {loading ? 'Asking...' : 'Ask'}
      </button>
      {answer && (
        <div className="qa-answer">
          <h4>Answer</h4>
          <p>{typeof answer === 'string' ? answer : answer.answer || JSON.stringify(answer)}</p>
        </div>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default QABox;
