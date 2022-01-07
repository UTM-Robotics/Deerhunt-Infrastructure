import React, { useState, useEffect } from "react";
import { Box, Heading, Container, Text, Stack } from "@chakra-ui/react";
import ConnectWithUs from "../components/ConnectWithUs";
import axios from "../config/config.js";

const HomeLoggedIn = (props) => {
  const [user, setUser] = useState("");

  useEffect(() => {
    axios.get("/api/user/info").then((response) => {
      setUser(response.data.email);
    });
  }, []);
  return (
    <>
      <Container maxW={"5xl"}>
        <Stack
          as={Box}
          textAlign={"center"}
          spacing={{ base: 6, md: 12 }}
          py={{ base: 20, md: 36 }}
        >
          <Heading
            fontWeight={700}
            fontSize={{ base: "2xl", sm: "4xl", md: "6xl" }}
            lineHeight={"110%"}
          >
            Welcome back, <br />
            <Text as={"span"} color={"orange.400"}>
              {user}
            </Text>
          </Heading>
          <Text color={"gray.500"}>
            This is a project maintained by the Robotics Club at the University
            of Toronto Mississauga. To learn more about this project, visit our
            Github.
          </Text>
          <Text as="i" color={"gray.500"}>
            Helping to bridge the gap between applied computer science and
            robotics.
          </Text>
          <Stack
            direction={"column"}
            spacing={3}
            align={"center"}
            alignSelf={"center"}
            position={"relative"}
          >
            <ConnectWithUs />
          </Stack>
        </Stack>
      </Container>
    </>
  );
};

export default HomeLoggedIn;
