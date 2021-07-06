import React from 'react'
import { Route, Switch } from 'react-router'

import Home from './pages/Home'
import HomeLoggedIn from './pages/HomeLoggedIn'
import Login from './pages/Login'
import Events from './pages/Events'
import Teams from './pages/Teams'
import Admin from './pages/Admin'
import NotFound from './pages/NotFound'

import history from './history'


class App extends React.Component {

    constructor(props) {
        super(props)
        this.state = { username: '', token: '' }
        this.handleLogin = this.handleLogin.bind(this)
    }

    handleLogin(user) {
        this.setState({ username: user })
        history.push('/')
    }


    render() {
        if (this.state.username !== '') {
            return <Switch>
                <Route path="/" component={() => <HomeLoggedIn username={this.state.username} />} exact />
                <Route path="/events" component={Events} />
                <Route path="/teams" component={Teams} />
                <Route path="/admin" component={Admin} />
                <Route component={NotFound} />
            </Switch>
        } else {
            return <Switch>
                <Route path="/" component={Home} exact />
                <Route path="/login" component={() => <Login onLogin={this.handleLogin} />} />
                <Route component={NotFound} />
            </Switch>
        }
    }
}

export default App