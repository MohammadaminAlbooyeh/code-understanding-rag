import { SET_ANALYSIS, SET_ANALYSES, SET_ANALYSIS_LOADING, SET_ANALYSIS_ERROR } from '../actions/analysisActions';

const initialState = { analyses: [], currentAnalysis: null, loading: false, error: null };

export function analysisReducer(state = initialState, action) {
  switch (action.type) {
    case SET_ANALYSIS:
      return { ...state, currentAnalysis: action.payload };
    case SET_ANALYSES:
      return { ...state, analyses: action.payload };
    case SET_ANALYSIS_LOADING:
      return { ...state, loading: action.payload };
    case SET_ANALYSIS_ERROR:
      return { ...state, error: action.payload };
    default:
      return state;
  }
}
