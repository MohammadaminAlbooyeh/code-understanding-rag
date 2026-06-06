export const SET_ANALYSIS = 'SET_ANALYSIS';
export const SET_ANALYSES = 'SET_ANALYSES';
export const SET_ANALYSIS_LOADING = 'SET_ANALYSIS_LOADING';
export const SET_ANALYSIS_ERROR = 'SET_ANALYSIS_ERROR';

export const setAnalysis = (analysis) => ({ type: SET_ANALYSIS, payload: analysis });
export const setAnalyses = (analyses) => ({ type: SET_ANALYSES, payload: analyses });
export const setAnalysisLoading = (loading) => ({ type: SET_ANALYSIS_LOADING, payload: loading });
export const setAnalysisError = (error) => ({ type: SET_ANALYSIS_ERROR, payload: error });
