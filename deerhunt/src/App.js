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
import MyEventsPage from "./pages/MyEventsPage";
import EventsPage from "./pages/EventsPage";
import TeamsPage from "./pages/TeamsPage";
import AmIAuthPage from "./pages/AmIAuthPage";
import axios from "./config/config";
import MyTeamsTable from "./components/MyTeamsTable";

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
      .catch((err) => {
      });
  }

  handleLogin(user) {
    this.setState({ email: user });
    history.push("/");
  }

  handleSignup(user) {
  }

  handleAdminLogin(user) {
    this.setState({ username: user });
    history.push("/admin");
  }

  render() {
    if (this.state.email !== "") {
      return (
        <Switch>
          <Route path="/login" component={() => <HomeLoggedIn />} exact />
          <Route path="/" component={() => <HomeLoggedIn />} exact />
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
          <Route path="/" component={() => <Home />} exact />
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
          <Route path="/events" component={EventsPage} />
          <Route path="/test" component={MyTeamsTable} />
          <Route path="/amiauth" component={AmIAuthPage} />
          <Route component={NotFound} />
        </Switch>
      );
    }
  }
}

export default App;
