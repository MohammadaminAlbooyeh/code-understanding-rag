import React, { useState } from 'react';

function QABox({ codeId }) {
  const [question, setQuestion] = useState('');

  return (
    <div className="qa-box">
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question about your code..."
      />
      <button>Ask</button>
    </div>
  );
}

export default QABox;
