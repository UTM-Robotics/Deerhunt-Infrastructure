import React, { useEffect, useState } from "react";
import { Box, Button, useDisclosure } from "@chakra-ui/react";
import SubmissionForm from "./SubmissionForm";

import TeamsTable from "./TeamsTable";
import AddTeamModal from "./AddTeamModal";
import axios from "../config/config";

export default function TeamsPanel(props) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [teamID, setTeamID] = useState("");
  const [teamsData, setTeamsData] = useState({});

  async function Submit(values) {
    let formData = new FormData();

    // TODO: revert submissions back to event name and team name cause it's easier
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

  // TODO: Fix this so that we get the team
  useEffect(() => {
    let form = new FormData();
    form.append("name", props.event);
    axios
      .post("/api/user/team", form)
      .then((response) => {
        console.log(response);
        setTeamsData(response.data);
      })
      .catch(() => {});
  }, []);
  return (
    <Box>
      <Box textAlign="left">
        <Button m={4} onClick={onOpen}>
          Create a New Team
        </Button>
        <AddTeamModal isOpen={isOpen} onClose={onClose} event={props.event} setTeamsData={setTeamsData} />
        <TeamsTable event={props.event} teamsData={teamsData} setTeamsData={setTeamsData}/>
        <SubmissionForm submissionCallback={Submit} />
      </Box>
    </Box>
  );
}
