import 'babel-polyfill';
import React from 'react';
import ReactDOM from 'react-dom';
import Routes from './routes';
import './assets/styles/style';
import { BrowserRouter} from 'react-router-dom';

// render the main component
ReactDOM.render(
    <BrowserRouter>
        <Routes />
    </BrowserRouter>,
  document.getElementById('app')
);
