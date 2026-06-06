import api from './api';

export const qaAPI = {
  ask: (codeId, question) => api.post('/qa', { code_id: codeId, question }),
  history: () => api.get('/qa/history'),
  batch: (questions) => api.post('/qa/batch', { questions }),
};
