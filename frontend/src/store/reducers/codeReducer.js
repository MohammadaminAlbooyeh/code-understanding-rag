import { SET_CODE, SET_CODES, SET_LOADING, SET_ERROR } from '../actions/codeActions';

const initialState = { codes: [], currentCode: null, loading: false, error: null };

export function codeReducer(state = initialState, action) {
  switch (action.type) {
    case SET_CODE:
      return { ...state, currentCode: action.payload };
    case SET_CODES:
      return { ...state, codes: action.payload };
    case SET_LOADING:
      return { ...state, loading: action.payload };
    case SET_ERROR:
      return { ...state, error: action.payload };
    default:
      return state;
  }
}
