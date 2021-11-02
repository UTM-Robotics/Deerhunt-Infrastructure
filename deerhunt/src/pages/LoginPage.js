import React from "react";
import LoginForm from "../components/LoginForm";
import AboutUs from "../components/AboutUs";
import { Grid, GridItem } from "@chakra-ui/react";
import ConnectWithUs from "../components/ConnectWithUs";

const LoginPage = () => {
  return (
    <Grid templateColumns="repeat(5, 1fr)">
      <GridItem colSpan={3} bg="gray.800">
        <AboutUs />
      </GridItem>
      <GridItem colSpan={2} bg="white">
        <LoginForm />
      </GridItem>
    </Grid>
  );
};

export default LoginPage;
