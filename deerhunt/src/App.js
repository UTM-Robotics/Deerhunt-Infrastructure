import React from 'react'
import { Route, Switch } from 'react-router'

import Home from './pages/Home'
import HomeLoggedIn from './pages/HomeLoggedIn'
import Login from './pages/Login'
import AdminLogin from './pages/AdminLogin'
import Events from './pages/Events'
import Teams from './pages/Teams'
import Admin from './pages/Admin'
import NotFound from './pages/NotFound'

import history from './history'


class App extends React.Component {

    constructor(props) {
        super(props)
        this.state = { email: '', username: '', token: '' }
        this.handleLogin = this.handleLogin.bind(this)
    }

    handleLogin(user) {
        this.setState({ email: user })
        history.push('/')
    }

    handleAdminLogin(user) {
        this.setState({ username: user })
        history.push('/admin')
    }


    render() {
        if (this.state.email !== '') {
            return <Switch>
                <Route path="/" component={() => <HomeLoggedIn email={this.state.email} />} exact />
                <Route path="/events" component={Events} />
                <Route path="/teams" component={Teams} />
                <Route path="/admin" component={Admin} />
                <Route component={NotFound} />
            </Switch>
        } else {
            return <Switch>
                <Route path="/" component={Home} exact />
                <Route path="/login" component={() => <Login onLogin={this.handleLogin} />} />
                <Route path="/adminlogin" component={() => <AdminLogin onLogin={this.handleLogin} />} />
                <Route component={NotFound} />
            </Switch>
        }
    }
}

export default App
