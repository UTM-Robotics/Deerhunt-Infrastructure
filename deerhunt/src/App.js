import React from "react";
import  {Route, Switch} from "react-router-dom";

import Home from "./pages/Home";
import HomeLoggedIn from "./pages/HomeLoggedIn";
import Events from "./pages/Events";
import Teams from "./pages/Teams";
import Admin from "./pages/Admin";
import NotFound from "./pages/NotFound";

import history from "./history";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import AdminLoginPage from "./pages/AdminLoginPage";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { email: "", username: "", token: "" };
    this.handleLogin = this.handleLogin.bind(this);
  }

  handleLogin(user) {
    this.setState({ email: user });
    history.push("/");
  }

  handleSignup(user) {
    console.log("signed up");
  }

  handleAdminLogin(user) {
    this.setState({ username: user });
    history.push("/admin");
  }

  render() {
    if (this.state.email !== "") {
      return (
        <Switch>
          <Route path="/" component={() => <HomeLoggedIn/>} exact />
          <Route path="/events" component={Events}/>  
          <Route path="/teams" component={Teams}/>
          <Route path="/admin" component={Admin}/>
          <Route component={NotFound} />
        </Switch>
      );
    } else {
      return (
        <Switch>
          <Route path="/" component={() => <Home/>} exact />
          <Route
            path="/login"
            component={() => <LoginPage onLogin={this.handleLogin} />}
          />
          <Route
            path="/signup"
            component={() => <SignUpPage onLogin={this.handleSignup} />}
          />
          <Route
            path="/adminlogin"
            component={() => <AdminLoginPage onLogin={this.handleLogin} />}
          />

          <Route component={NotFound} />
        </Switch>
      );
    }
  }
}

export default App;
