import { Heading, Stack, Text } from "@chakra-ui/react";
import axios from "../config/config.js";
import React, { useState, useEffect } from "react";

const EventDetailsPanel = (props) => {
  const [eventData, setEventData] = useState({});

  useEffect(() => {
    axios
      .get("/api/events", { params: { name: props.event } })
      .then((response) => {
        setEventData(response.data);
      });
  }, []);

  return (
    <Stack>
      <Heading fontSize={{ base: "xl", sm: "2xl", md: "3xl" }}>Game</Heading>
      <Text>{eventData.game}</Text>
      <Heading fontSize={{ base: "xl", sm: "2xl", md: "3xl" }}>
        Description
      </Heading>
      <Text>{eventData.description}</Text>
      <Heading fontSize={{ base: "xl", sm: "2xl", md: "3xl" }}>
        Start Time
      </Heading>
      <Text>{eventData.starttime}</Text>
      <Heading fontSize={{ base: "xl", sm: "2xl", md: "3xl" }}>
        End Time
      </Heading>
      <Text>{eventData.endtime}</Text>
    </Stack>
  );
};

export default EventDetailsPanel;
