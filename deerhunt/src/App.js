import React from "react";
import { Route, Switch, Redirect } from "react-router";

import Home from "./pages/Home";
import HomeLoggedIn from "./pages/HomeLoggedIn";
import Admin from "./pages/Admin";
import NotFound from "./pages/NotFound";
import history from "./history";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import AdminLoginPage from "./pages/AdminLoginPage";
import ResetPasswordPage from "./pages/ResetPasswordPage";
import MyEventsPage from "./pages/MyEventsPage";
import EventsPage from "./pages/EventsPage";
import TeamsPage from "./pages/TeamsPage";

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
          <Route
            path="/"
            component={
              <HomeLoggedIn email={this.state.email} isLoggedIn={true} />
            }
            exact
          />
          <Route path="/events" component={EventsPage} />
          <Route path="/myevents" component={MyEventsPage} />
          <Route path="/teams" component={TeamsPage} />
          <Route path="/admin" component={Admin} />
          <Route component={NotFound} />
        </Switch>
      );
    } else {
      return (
        <Switch>
          <Route path="/" component={Home} exact />
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
          <Route path="/forgotpassword" component={ResetPasswordPage} />
          <Route component={NotFound} />
        </Switch>
      );
    }
  }
}

export default App;
