import React, { useEffect, useState } from "react";
import { Box, Button, Heading, useDisclosure, Stack } from "@chakra-ui/react";
import SubmissionForm from "./SubmissionForm";

import TeamsTable from "./TeamsTable";
import AddTeamModal from "./AddTeamModal";
import axios from "../config/config";
import MatchList from "./MatchList";

export default function TeamsPanel(props) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [teamsData, setTeamsData] = useState({});

  async function Submit(values) {
    let formData = new FormData();

    // TODO: revert submissions back to event name and team name cause it's easier
    formData.append("file", values[0]);
    formData.append("event_name", props.event);
    formData.append("team_name", teamsData.name);

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
    <Box m={4}>
      {teamsData._id ? (
        <Stack textAlign={"center"} spacing={12}>
          <TeamsTable
            event={props.event}
            teamsData={teamsData}
            setTeamsData={setTeamsData}
          />
          <SubmissionForm submissionCallback={Submit} />
          <MatchList event={props.event} />
        </Stack>
      ) : (
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
      )}
    </Box>
  );
}
