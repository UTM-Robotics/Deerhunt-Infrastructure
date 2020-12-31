import React from 'react';
import { Route, Switch } from 'react-router-dom';
import AppWrapper from './components/App';
import Home from './components/Home';
import Login from './components/Login';
import Replay from './components/GameReplay';
import Submit from './components/Submit';
import AdminPanel from './components/AdminPanel';
import ErrorPage from './components/ErrorPage';
import Profile from './components/Profile';
import Register from './components/Register';

class Routes extends React.Component {
    render() {
        return (
            <AppWrapper>
                <Switch>
                    <Route exact path='/' component={Login} />
                    <Route path='/deerhunt' component={Login} />
                    <Route path='/register' component={Register} />
                    <Route path='/home' component={Home} />
                    <Route path='/replay' component={Replay} />
                    <Route path='/submit' component={Submit} />
                    <Route path='/88388' component={AdminPanel} />
                    <Route path='/profile' component={Profile} />
                    <Route path='*' component={ErrorPage} />
                </Switch>
            </AppWrapper>
        );
    }
}

export default Routes;
