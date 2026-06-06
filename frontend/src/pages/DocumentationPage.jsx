import React from 'react';
import { useParams } from 'react-router-dom';
import DocumentationViewer from '../components/DocumentationViewer';

function DocumentationPage() {
  const { id } = useParams();
  return (
    <div className="documentation-page">
      <h1>Documentation</h1>
      <DocumentationViewer docId={id} />
    </div>
  );
}

export default DocumentationPage;
