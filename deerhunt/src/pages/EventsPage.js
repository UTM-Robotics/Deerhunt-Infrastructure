import React from "react";
import { Box, Heading } from "@chakra-ui/react";
import TopNav from "../components/TopNav";
import ComingSoonCard from "../components/ComingSoonCard";

export default function EventsPage() {
  return (
    <Box justifyContent={"left"}>
      <TopNav />
      <Box>
        <ComingSoonCard />
      </Box>
    </Box>
  );
}
