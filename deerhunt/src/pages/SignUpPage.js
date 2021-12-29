import React, {useState} from "react";
import SignUpForm from "../components/SignUpForm";
import AboutUs from "../components/AboutUs";
import { Flex, Stack} from "@chakra-ui/react";
import SignUpAlert from "../components/SignUpAlert";

export default function SignUpPage(){
  const [error1, setError] = useState(null);
  return (
    <Stack minH={"100vh"} direction={{ base: "column", md: "row" }}>
      <Flex flex={2}>
        <AboutUs />
      </Flex>
      <Flex p={8} flex={1} align={"center"} justify={"center"}>
        <Stack spacing={4} w={"full"} maxW={"md"}>
          <SignUpAlert error1={error1} setError={setError} />
          <SignUpForm error1={error1} setError={setError}/>
       
        </Stack>
      </Flex>
    </Stack>
  );
}; 