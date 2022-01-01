import React from "react";
import { Box } from "@chakra-ui/react";
import TopNav from "../components/TopNav";
import EventList from "../components/EventList";

export default function EventsPage() {
  return (
    <Box justifyContent={"left"}>
      <TopNav />
      <Box>
        <EventList />
      </Box>
    </Box>
  );
}
