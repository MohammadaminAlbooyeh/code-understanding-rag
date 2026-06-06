import { SET_QA, SET_QA_HISTORY, SET_QA_LOADING, SET_QA_ERROR } from '../actions/qaActions';

const initialState = { history: [], currentQA: null, loading: false, error: null };

export function qaReducer(state = initialState, action) {
  switch (action.type) {
    case SET_QA:
      return { ...state, currentQA: action.payload };
    case SET_QA_HISTORY:
      return { ...state, history: action.payload };
    case SET_QA_LOADING:
      return { ...state, loading: action.payload };
    case SET_QA_ERROR:
      return { ...state, error: action.payload };
    default:
      return state;
  }
}
