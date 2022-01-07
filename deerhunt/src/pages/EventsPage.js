import React from "react";
import { Box } from "@chakra-ui/react";
import EventList from "../components/EventList";

export default function EventsPage() {
  return (
    <Box justifyContent={"left"}>
      <Box>
        <EventList />
      </Box>
    </Box>
  );
}
