import React from "react";
import axios from "axios";
import Navbar from "./MenuBar/Navbar";
import { Flex, Input, Button, Box, Heading } from "@chakra-ui/react";
import { FormControl, FormLabel } from "@chakra-ui/react";

class Signup extends React.Component {
  constructor(props) {
    super(props);
    this.state = { email: "", password: "" };

    console.log(props);

    this.handleInputChange = this.handleInputChange.bind(this);
    this.CreateUser = this.CreateUser.bind(this);
  }

  handleInputChange(event) {
    const name = event.target.name;
    this.setState({ [name]: event.target.value });
  }

  CreateUser() {
    axios
      .post("http://localhost:5000/api/register", {
        email: this.state.email,
        password: this.state.password,
      })
      .then((resp) => {
        console.log(resp);
        this.props.onLogin(this.state.email);
      })
      .catch((err) => {
        console.log(err);
      });
    console.log("Creating user");
  }

  render() {
    return (
      <Flex
        minHeight="100vh"
        width="full"
        justifyContent="center"
        alignItems="center"
      >
        <Box>
          <Box
            borderWidth={1}
            px={6}
            py={6}
            borderRadius={4}
            boxShadow="lg"
            width="full"
            maxWidth="500px"
            bg="gray.300"
          >
            <Box textAlign="center" mb={4}>
              <Heading>Welcome back!</Heading>
            </Box>
            <Box>
              <form>
                <FormControl>
                  <FormLabel>Email</FormLabel>
                  <Input type="email" placeholder="Enter Your Email" />
                </FormControl>
                <FormControl mt={4}>
                  <FormLabel>Password</FormLabel>
                  <Input type="password" placeholder="Enter Your Password" />
                </FormControl>
                <Box my={4}>
                  <Button width="full" type="submit">
                    Login
                  </Button>
                </Box>
                <Box my={4}>
                  <Button width="full">Create An Account</Button>
                </Box>
              </form>
            </Box>
          </Box>
        </Box>
      </Flex>
    );
  }
}

export default Signup;
