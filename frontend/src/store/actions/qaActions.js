export const SET_QA = 'SET_QA';
export const SET_QA_HISTORY = 'SET_QA_HISTORY';
export const SET_QA_LOADING = 'SET_QA_LOADING';
export const SET_QA_ERROR = 'SET_QA_ERROR';

export const setQA = (qa) => ({ type: SET_QA, payload: qa });
export const setQaHistory = (history) => ({ type: SET_QA_HISTORY, payload: history });
export const setQaLoading = (loading) => ({ type: SET_QA_LOADING, payload: loading });
export const setQaError = (error) => ({ type: SET_QA_ERROR, payload: error });
