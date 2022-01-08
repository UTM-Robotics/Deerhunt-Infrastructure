import React from "react";
import { Box, Heading, Container, Text, Stack } from "@chakra-ui/react";
import ConnectWithUs from "../components/ConnectWithUs";

const Home = () => {
  return (
    <>
      <Container maxW={"3xl"}>
        <Stack
          as={Box}
          textAlign={"center"}
          spacing={{ base: 6, md: 12 }}
          py={{ base: 20, md: 36 }}
        >
          <Heading
            fontWeight={700}
            fontSize={{ base: "4xl", sm: "6xl", md: "8xl" }}
            lineHeight={"110%"}
          >
            Deerhunt <br />
            <Text as={"span"} color={"orange.400"}>
              Infrastructure
            </Text>
          </Heading>
          <Text>
            This is a project maintained by the Robotics Club at the University
            of Toronto Mississauga. To learn more about this project, visit our
            Github.
          </Text>
          <Text as="i">
            Helping to bridge the gap between applied computer science and
            robotics
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

export default Home;
