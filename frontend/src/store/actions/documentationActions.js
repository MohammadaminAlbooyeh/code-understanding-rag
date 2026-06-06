export const SET_DOCUMENTATION = 'SET_DOCUMENTATION';
export const SET_DOCUMENTATION_LOADING = 'SET_DOCUMENTATION_LOADING';
export const SET_DOCUMENTATION_ERROR = 'SET_DOCUMENTATION_ERROR';

export const setDocumentation = (doc) => ({ type: SET_DOCUMENTATION, payload: doc });
export const setDocumentationLoading = (loading) => ({ type: SET_DOCUMENTATION_LOADING, payload: loading });
export const setDocumentationError = (error) => ({ type: SET_DOCUMENTATION_ERROR, payload: error });
