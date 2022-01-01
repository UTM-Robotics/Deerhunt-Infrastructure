import React from "react";
import axios from "../config/config";

class Home extends React.Component {
  constructor(props) {
    super(props);

    this.all_events = [];
  }

  get_events() {
    axios
      .get("http://localhost:5000/api/amiauth")
      .then((resp) => {
        console.log(resp.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }

  render() {
    console.log("rendering");
    return <div>{this.get_events()}</div>;
  }
}

export default Home;
