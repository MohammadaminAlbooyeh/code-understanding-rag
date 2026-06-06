import api from './api';

export const codeAPI = {
  upload: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/code/upload', formData);
  },
  list: () => api.get('/code'),
  get: (id) => api.get(`/code/${id}`),
  delete: (id) => api.delete(`/code/${id}`),
};
