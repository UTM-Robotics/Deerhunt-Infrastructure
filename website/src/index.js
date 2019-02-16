import 'babel-polyfill';
import React from 'react';
import ReactDOM from 'react-dom';
import { routes } from './routes';
import './assets/styles/style';

// render the main component
ReactDOM.render(
  <Provider store={store}>
      {routes}
  </Provider>,
  document.getElementById('app')
);
