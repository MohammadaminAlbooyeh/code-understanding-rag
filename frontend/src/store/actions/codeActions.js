export const SET_CODE = 'SET_CODE';
export const SET_CODES = 'SET_CODES';
export const SET_LOADING = 'SET_LOADING';
export const SET_ERROR = 'SET_ERROR';

export const setCode = (code) => ({ type: SET_CODE, payload: code });
export const setCodes = (codes) => ({ type: SET_CODES, payload: codes });
export const setLoading = (loading) => ({ type: SET_LOADING, payload: loading });
export const setError = (error) => ({ type: SET_ERROR, payload: error });
