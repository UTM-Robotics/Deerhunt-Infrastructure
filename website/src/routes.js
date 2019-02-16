import React from 'react';
import { Route, Switch } from 'react-router-dom';
import AppWrapper from './components/App';
import Home from './components/Home';
import About from './components/About';
import Login from './components/Login';

class Routes extends React.Component {
    render() {
        return (
            <AppWrapper>
                <Switch>
                    <Route exact path='/' component={Home} />
                    <Route path='/about' component={About} />
                    <Route exact path='/login' component={Login} />
                </Switch>
            </AppWrapper>
        );
    }
}

export default Routes;
