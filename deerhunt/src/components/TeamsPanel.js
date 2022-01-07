import React, { useEffect, useState } from "react";
import { Box, Button, Heading, useDisclosure } from "@chakra-ui/react";
import SubmissionForm from "./SubmissionForm";

import TeamsTable from "./TeamsTable";
import AddTeamModal from "./AddTeamModal";
import axios from "../config/config";

export default function TeamsPanel(props) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [teamID, setTeamID] = useState("");

  async function Submit(values) {
    let formData = new FormData();

    formData.append("file", values[0]);
    formData.append("event_id", props.event);
    formData.append("team_id", teamID);

    await axios
      .post("api/submissions", formData)
      .then((response) => {
        console.log("Submission succeeded");
      })
      .catch(() => {});
  }

  useEffect(() => {
    axios
      .get("/api/teams", { params: { game: props.event } })
      .then((response) => {
        setTeamID(response.data._id["$oid"]);
        console.log(response);
      })
      .catch(() => {});
  }, []);

  return (
    <Box m={4}>
      {teamID === "" ? (
        <Box textAlign="center">
          <Heading fontSize={{ base: "xl", sm: "2xl", md: "3xl" }}>
            You're not currently in a team for this event.
          </Heading>
          <Button m={4} onClick={onOpen}>
            Create a New Team
            <AddTeamModal
              isOpen={isOpen}
              onClose={onClose}
              event={props.event}
            />
          </Button>
        </Box>
      ) : (
        <Box textAlign={"center"}>
          <TeamsTable event={props.event} />
          <SubmissionForm submissionCallback={Submit} />
        </Box>
      )}
    </Box>
  );
}
