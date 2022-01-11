import React, { useState, useEffect } from "react";
import { Box, Heading, Text, VStack } from "@chakra-ui/react";
import ConnectWithUs from "../components/ConnectWithUs";
import axios from "../config/config.js";
import ProjectContributors from "../components/ProjectContributors";
import { FaLongArrowAltDown } from "react-icons/fa";

const HomeLoggedIn = () => {
  const [user, setUser] = useState("");

  useEffect(() => {
    axios.get("/api/user/info").then((response) => {
      setUser(response.data.email);
    });
  }, []);

  return (
    <>
      <Box minH="100vh" textAlign={"center"}>
        <VStack
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
          <Text>
            This is a project maintained by the Robotics Club at the University
            of Toronto Mississauga. To learn more about this project, visit our
            Github.
          </Text>
          <Text as="i">
            Helping to bridge the gap between applied computer science and
            robotics
          </Text>
          <ConnectWithUs />
        </VStack>
        <Box bottom={0} textAlign={"center"}>
          <VStack>
            <Text as="b">Scroll to learn more!</Text>
            <FaLongArrowAltDown />
          </VStack>
        </Box>
      </Box>
      <Box minH="100vh">
        <VStack
          spacing={3}
          align={"center"}
          alignSelf={"center"}
          position={"relative"}
          mt={8}
        >
          <ProjectContributors />
        </VStack>
      </Box>
    </>
  );
};

export default HomeLoggedIn;
