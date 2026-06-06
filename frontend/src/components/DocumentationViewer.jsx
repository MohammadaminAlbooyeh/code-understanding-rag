import React, { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { documentationAPI } from '../services/documentation_api';

function DocumentationViewer({ docId }) {
  const [doc, setDoc] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!docId) return;
    setLoading(true);
    documentationAPI.get(docId)
      .then((res) => setDoc(res.data || res))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [docId]);

  if (!docId) return <div className="documentation-viewer"><p>No document selected.</p></div>;
  if (loading) return <div className="documentation-viewer"><p>Loading documentation...</p></div>;
  if (error) return <div className="documentation-viewer"><p className="error">{error}</p></div>;

  const content = typeof doc === 'string' ? doc : doc.content || doc.markdown || JSON.stringify(doc);

  return (
    <div className="documentation-viewer">
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  );
}

export default DocumentationViewer;
