import React from "react";
import LoginForm from "../components/LoginForm";
import AboutUs from "../components/AboutUs";
import { Flex, Stack} from "@chakra-ui/react";
import SignUpAlert from "../components/SignUpAlert";

const LoginPage = (props) => {
  return (
    <Stack minH={"100vh"} direction={{ base: "column", md: "row" }}>
      <Flex flex={2}>
        <AboutUs/>
      </Flex>
      <Flex p={8} flex={1} align={"center"} justify={"center"}>
        <Stack spacing={4} w={"full"} maxW={"md"}>
          <SignUpAlert />
          <LoginForm onLogin={props.onLogin}/>
        </Stack>
      </Flex>
    </Stack>
  );
};

export default LoginPage;
