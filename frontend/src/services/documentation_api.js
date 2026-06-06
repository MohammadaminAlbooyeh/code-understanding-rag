import api from './api';

export const documentationAPI = {
  generate: (codeId, docType) => api.post('/docs/generate', { code_id: codeId, doc_type: docType }),
  get: (id) => api.get(`/docs/${id}`),
  export: (id, format) => api.post('/docs/export', { id, format }),
};
