import React from 'react';
import { Route, Switch } from 'react-router-dom';
import AppWrapper from './components/App';
import Home from './components/Home';
import About from './components/About';
import Login from './components/Login';
import Replay from './components/GameReplay';
import Submit from './components/Submit';

class Routes extends React.Component {
    render() {
        return (
            <AppWrapper>
                <Switch>
                    <Route exact path='/' component={Home} />
                    <Route path='/about' component={About} />
                    <Route path='/login' component={Login} />
                    <Route path='/replay' component={Replay} />
                    <Route path='/submit' component={Submit} />
                </Switch>
            </AppWrapper>
        );
    }
}

export default Routes;
