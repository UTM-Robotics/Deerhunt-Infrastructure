import React from "react";
import { Alert, AlertIcon, AlertDescription } from "@chakra-ui/react";

const FeedbackAlert = (props) => {
  return (
    <Alert status={props.status}>
      <AlertIcon />
      <AlertDescription>{props.description}</AlertDescription>
    </Alert>
  );
};

export default FeedbackAlert;
