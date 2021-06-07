import React from 'react'
import { Route, Switch } from 'react-router'

import Home from './pages/Home'
import Login from './pages/Login'
import Events from './pages/Events'
import Teams from './pages/Teams'
import Admin from './pages/Admin'
import NotFound from './pages/NotFound'

class App extends React.Component {
    render() {
        return ( 
            <main>
                <Switch>
                    <Route path="/" component={Home} exact />
                    <Route path="/login" component={Login}  />
                    <Route path="/events" component={Events}  />
                    <Route path="/teams" component={Teams}  />
                    <Route path="/admin" component={Admin}  />
                    <Route component={NotFound}  />
                </Switch>
            </main> 
        )
    }
}

export default App