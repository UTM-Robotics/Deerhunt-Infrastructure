import React from "react";
import { Box, Heading } from "@chakra-ui/react";
import TopNav from "../components/TopNav";

export default function MyEventsPage() {
  return (
    <Box>
      <TopNav $isloggedin={true} />
      <Box textAlign="center">
        <Heading>Coming soon!</Heading>
      </Box>
    </Box>
  );
}
