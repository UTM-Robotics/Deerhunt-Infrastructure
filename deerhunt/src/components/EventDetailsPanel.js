import { Text } from "@chakra-ui/react";
import axios from "axios";
import React, { useState } from "react";

const EventDetailsPanel = (props) => {
  const [eventData, setEventData] = useState(null);

  const getEvent = () => {
    axios.get("/api/events", props.event).then((response) => {
      setEventData(response.data);
    }, console.log(eventData));
  };
  return <Text>{props.event}</Text>;
};

export default EventDetailsPanel;
