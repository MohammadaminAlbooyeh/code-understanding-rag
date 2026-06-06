import api from './api';

export const analysisAPI = {
  parse: (codeId) => api.post('/analysis/parse', { code_id: codeId }),
  complexity: (codeId) => api.post('/analysis/complexity', { code_id: codeId }),
  bugs: (codeId) => api.post('/analysis/bugs', { code_id: codeId }),
  security: (codeId) => api.post('/analysis/security', { code_id: codeId }),
  get: (id) => api.get(`/analysis/${id}`),
};
