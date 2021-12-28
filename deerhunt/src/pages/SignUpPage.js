import React from "react";
import SignUpForm from "../components/SignUpForm";
import AboutUs from "../components/AboutUs";
import { Flex, Stack } from "@chakra-ui/react";

const SignUpPage = () => {
  return (
    <Stack minH={"100vh"} direction={{ base: "column", md: "row" }}>
      <Flex flex={2}>
        <AboutUs />
      </Flex>
      <Flex p={8} flex={1} align={"center"} justify={"center"}>
        <Stack spacing={4} w={"full"} maxW={"md"}>
          <SignUpForm />
        </Stack>
      </Flex>
    </Stack>
  );
};

export default SignUpPage;
