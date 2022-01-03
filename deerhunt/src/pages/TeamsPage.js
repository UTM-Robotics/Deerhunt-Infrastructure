import React from "react";
import { Box } from "@chakra-ui/react";
import TopNav from "../components/TopNav";
import ComingSoon from "../components/ComingSoon";

export default function TeamsPage() {
  return (
    <Box>
        <TopNav isloggedin={+true}/>
      <Box textAlign="center">
        <ComingSoon />
      </Box>
    </Box>
  );
}
