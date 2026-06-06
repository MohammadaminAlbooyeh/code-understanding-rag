import React, { useState } from 'react';

function CodeUploader() {
  const [file, setFile] = useState(null);

  const handleUpload = () => {
  };

  return (
    <div className="code-uploader">
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>
    </div>
  );
}

export default CodeUploader;
