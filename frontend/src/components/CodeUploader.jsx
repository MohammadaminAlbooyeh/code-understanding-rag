import React, { useState } from 'react';
import { useCodeUpload } from '../hooks/useCodeUpload';

function CodeUploader() {
  const [file, setFile] = useState(null);
  const { upload, loading, error } = useCodeUpload();

  const handleUpload = async () => {
    if (!file) return;
    try {
      await upload(file);
      setFile(null);
    } catch (err) {
      console.error('Upload failed:', err);
    }
  };

  return (
    <div className="code-uploader">
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} disabled={loading || !file}>
        {loading ? 'Uploading...' : 'Upload'}
      </button>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default CodeUploader;
