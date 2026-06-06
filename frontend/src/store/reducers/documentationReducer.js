import { SET_DOCUMENTATION, SET_DOCUMENTATION_LOADING, SET_DOCUMENTATION_ERROR } from '../actions/documentationActions';

const initialState = { currentDoc: null, loading: false, error: null };

export function documentationReducer(state = initialState, action) {
  switch (action.type) {
    case SET_DOCUMENTATION:
      return { ...state, currentDoc: action.payload };
    case SET_DOCUMENTATION_LOADING:
      return { ...state, loading: action.payload };
    case SET_DOCUMENTATION_ERROR:
      return { ...state, error: action.payload };
    default:
      return state;
  }
}
