import React, { useState } from "react";
import SignUpForm from "../components/SignUpForm";
import { Flex, Stack, Image } from "@chakra-ui/react";
import SignUpAlert from "../components/SignUpAlert";
import background from "../images/background.png";
import ColourModeToggle from "../components/ColourModeToggle";

export default function SignUpPage() {
  const [error1, setError] = useState(null);
  return (
    <Stack minH={"100vh"} direction={{ base: "column", md: "row" }}>
      <Flex flex={2}>
        <Image
          alt={"Cool robotics background image"}
          objectFit={"cover"}
          src={background}
        />
      </Flex>
      <Flex p={8} flex={1} align={"center"} justify={"center"}>
        <Stack spacing={4} w={"full"} maxW={"md"}>
          <SignUpAlert error1={error1} setError={setError} />
          <SignUpForm error1={error1} setError={setError} />
        </Stack>
      </Flex>
      <ColourModeToggle />
    </Stack>
  );
}
