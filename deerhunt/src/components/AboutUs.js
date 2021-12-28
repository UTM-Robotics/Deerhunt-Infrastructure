import React from "react";
import { Heading, Text, Box, Flex } from "@chakra-ui/react";
import ConnectWithUs from "./ConnectWithUs";

const AboutUs = () => {
  return (
    <Flex
      minHeight="80vh"
      width="full"
      justifyContent="center"
      alignItems="center"
      bg="#011627"
    >
      <Box maxWidth="500px" mx={4}>
        <Heading color="white">Welcome to the Deerhunt Infrastructure</Heading>
        <Text pt={4} color="white">
          This is a project maintained by the Robotics Club at the University of
          Toronto Mississauga. To learn more about this project, visit our
          Github.
        </Text>
        <ConnectWithUs />
      </Box>
    </Flex>
  );
};

export default AboutUs;
