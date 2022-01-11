import React from "react";
import { Route, Switch } from "react-router-dom";

import Home from "./pages/Home";
import HomeLoggedIn from "./pages/HomeLoggedIn";
import Admin from "./pages/Admin";
import NotFound from "./pages/NotFound";
import history from "./history";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";
import AdminLoginPage from "./pages/AdminLoginPage";
import ResetPasswordPage from "./pages/ResetPasswordPage";
import EventsPage from "./pages/EventsPage";
import axios from "./config/config";
import EventUserPage from "./pages/EventUserPage";
import { LoginLayout, GeneralLayout } from "./components/Layout";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { email: "", username: "", token: "" };
    this.handleLogin = this.handleLogin.bind(this);
  }

  componentDidMount() {
    if (localStorage.getItem("token")) {
      axios.defaults.headers.common["Authorization"] =
        "Bearer " + localStorage.getItem("token");
      /*console.log("set token");*/
    }
    axios
      .get("/api/user/info")
      .then((resp) => {
        this.setState({ email: resp.data.email });
      })
      .catch((err) => {});
  }

  handleLogin(user) {
    this.setState({ email: user });
    history.push("/");
  }

  handleSignup(user) {}

  handleAdminLogin(user) {
    this.setState({ username: user });
    history.push("/admin");
  }

  render() {
    if (this.state.email !== "") {
      return (
        <Switch>
          <RouteWrapper
            path="/login"
            component={() => <HomeLoggedIn />}
            exact
            layout={LoginLayout}
          />
          <RouteWrapper
            path="/signup"
            component={() => <HomeLoggedIn />}
            exact
            layout={LoginLayout}
          />
          <RouteWrapper
            path="/"
            component={() => <HomeLoggedIn />}
            exact
            layout={GeneralLayout}
          />
          <RouteWrapper
            exact
            path="/events"
            component={EventsPage}
            layout={GeneralLayout}
          />
          <RouteWrapper
            exact
            path="/events/:event"
            component={EventUserPage}
            layout={GeneralLayout}
          />

          {/*<Route path="/myevents" component={MyEventsPage} />*/}
          {/*<Route path="/teams" component={TeamsPage} />*/}
          <Route path="/admin" component={Admin} />
          <RouteWrapper
            path="/notfound"
            component={NotFound}
            layout={LoginLayout}
          />
        </Switch>
      );
    } else {
      return (
        <Switch>
          <RouteWrapper
            path="/"
            component={() => <Home />}
            exact
            layout={GeneralLayout}
          />
          <RouteWrapper
            path="/login"
            component={() => <LoginPage onLogin={this.handleLogin} />}
            layout={LoginLayout}
          />
          <RouteWrapper
            path="/signup"
            component={() => <SignUpPage onLogin={this.handleSignup} />}
            layout={LoginLayout}
          />
          <RouteWrapper
            path="/adminlogin"
            component={() => <AdminLoginPage onLogin={this.handleLogin} />}
            layout={LoginLayout}
          />
          <RouteWrapper
            path="/forgotpassword"
            component={ResetPasswordPage}
            layout={LoginLayout}
          />
          <RouteWrapper
            exact
            path="/events"
            component={EventsPage}
            layout={GeneralLayout}
          />
          <RouteWrapper
            exact
            path="/events/:event"
            component={EventUserPage}
            layout={GeneralLayout}
          />
          {/*<Route path="/test" component={EventUserPage} />*/}
          {/*<Route path="/amiauth" component={AmIAuthPage} />*/}
          <RouteWrapper
            path="/notfound"
            component={NotFound}
            layout={LoginLayout}
          />
        </Switch>
      );
    }
  }
}
function RouteWrapper({ component: Component, layout: Layout, ...rest }) {
  return (
    <Route
      {...rest}
      render={(props) => (
        <Layout {...props}>
          <Component {...props} />
        </Layout>
      )}
    />
  );
}

export default App;
