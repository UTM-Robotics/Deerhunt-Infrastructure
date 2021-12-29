import React from 'react';
import ReactDOM from 'react-dom';
import reportWebVitals from './reportWebVitals';
import { Router } from 'react-router-dom'
import { ChakraProvider } from "@chakra-ui/react"
import theme from './theme'

import history from "./history";
import App from './App.js'
import { StateProvider } from './statemanager/StateProvider';
import SignUpReducer, { initialState } from './statemanager/SignUpStatusReducer';

ReactDOM.render(
      <ChakraProvider theme={theme}>
        <Router history={history}>
          <StateProvider initialState={initialState} reducer={SignUpReducer}>
            <App />
          </StateProvider>
          
        </Router>
      </ChakraProvider>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
