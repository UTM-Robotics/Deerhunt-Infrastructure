import { Text, Box } from "@chakra-ui/react";
import axios from "../config/config.js";
import React, { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import ChakraUIRenderer from "chakra-ui-markdown-renderer";

const TutorialPanel = (props) => {
  const [tutorial, setTutorial] = useState("");

  useEffect(() => {
    axios
      .get("/api/events", { params: { game: props.event } })
      .then((response) => {
        setTutorial(response.data.tutorial);
      });
  }, []);

  return (
    <div>
      <ReactMarkdown
        components={ChakraUIRenderer()}
        children={tutorial}
        skipHtml
      />
    </div>
  );
};

export default TutorialPanel;
