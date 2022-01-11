import { Box, Heading } from "@chakra-ui/react";
import React from "react";
import Contributors from "react-contributors";

const ProjectContributors = () => {
  const owner = "UTM-Robotics";
  const repos = ["Deerhunt-Infrastructure"];
  return (
    <Box textAlign={"center"} m={6}>
      <Heading>Meet Our Contributors</Heading>
      <Contributors owner={owner} repo={repos} />
    </Box>
  );
};

export default ProjectContributors;
