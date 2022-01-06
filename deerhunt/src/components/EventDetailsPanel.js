import { Heading, Stack, Text } from "@chakra-ui/react";
import axios from "../config/config.js";
import React, { useState, useEffect } from "react";

const EventDetailsPanel = (props) => {
  const [eventData, setEventData] = useState({});

  useEffect(() => {
    axios
      .get("/api/events", { params: { game: props.event } })
      .then((response) => {
        setEventData(response.data);
      });
  }, []);

  return (
    <Stack>
      <Heading>Game</Heading>
      <Text>{eventData.game}</Text>
      <Heading>Description</Heading>
      <Text>{eventData.description}</Text>
      <Heading>Start Time</Heading>
      <Text>{eventData.starttime}</Text>
      <Heading>End Time</Heading>
      <Text>{eventData.endtime}</Text>
    </Stack>
  );
};

export default EventDetailsPanel;
