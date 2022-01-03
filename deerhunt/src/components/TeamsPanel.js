import React, { useState } from "react";
import { Box, Button, useDisclosure } from "@chakra-ui/react";
import SubmissionForm from "./SubmissionForm";

import TeamsTable from "./TeamsTable";
import AddTeamModal from "./AddTeamModal";
import axios from "axios";

export default function TeamsPanel(props) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [teamID, setTeamID] = useState("");

  async function Submit(values) {
    let formData = new FormData();

    formData.append("file", values[0]);
    formData.append("event_id", props.event);
    formData.append("team_id", teamID);

    await axios
      .post("api/submissions", form)
      .then((response) => {
        console.log("Submission succeeded");
      })
      .catch(() => {});
  }

  await axios
    .get("api/user/info")
    .then((response) => {
      console.log(response);
    })
    .catch(() => {});
  return (
    <Box>
      <Box textAlign="left">
        <Button m={4} onClick={onOpen}>
          Create a New Team
        </Button>
        <AddTeamModal isOpen={isOpen} onClose={onClose} />
        <TeamsTable />
        <SubmissionForm submissionCallback={Submit} />
      </Box>
    </Box>
  );
}
