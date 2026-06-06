import { createStore, applyMiddleware, combineReducers } from 'redux';
import { thunk } from 'redux-thunk';
import { codeReducer } from './reducers/codeReducer';
import { analysisReducer } from './reducers/analysisReducer';
import { documentationReducer } from './reducers/documentationReducer';
import { qaReducer } from './reducers/qaReducer';

const rootReducer = combineReducers({
  code: codeReducer,
  analysis: analysisReducer,
  documentation: documentationReducer,
  qa: qaReducer,
});

export const store = createStore(rootReducer, applyMiddleware(thunk));
