import React from "react";
import TopNav from "../components/TopNav";
import { Heading, Box } from "@chakra-ui/react";

class Home extends React.Component {
  constructor(props) {
    super(props);

    this.state = { email: props.email };
  }

  render() {
    return (
      <div>
        <TopNav isloggedin={true} />
        <Box textAlign="center" mt={"12px"}>
          <Heading>The UTM AI Competition Hub</Heading>

          <h3>Welcome {this.state.email}</h3>
        </Box>
      </div>
    );
  }
}

export default Home;
