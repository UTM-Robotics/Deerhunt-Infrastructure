import React from "react";
import TopNav from "../components/TopNav";
import { Heading, Box, Text } from "@chakra-ui/react";
import axios from "../config/config";

class Home extends React.Component {
  constructor(props) {
    super(props);

    this.all_events = [];
  }

  get_events() {
    axios
      .get("http://127.0.0.1:5000/api/events")
      .then((resp) => {
        console.log(resp.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }

  render() {
    console.log("rendering");
    return (
      <div>
        <TopNav />
        <Box textAlign="center" mt={"12px"}>
          <Heading>The UTM AI Competition Hub</Heading>
          <Text mt={"12px"}>Login to join the fun!</Text>
        </Box>
        {this.get_events()}
      </div>
    );
  }
}

export default Home;
