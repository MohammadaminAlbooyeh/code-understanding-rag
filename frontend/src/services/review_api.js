import api from './api';

export const reviewAPI = {
  review: (codeId) => api.post('/review', { code_id: codeId }),
  get: (id) => api.get(`/review/${id}`),
  refactor: (codeId) => api.post('/refactor', { code_id: codeId }),
};
