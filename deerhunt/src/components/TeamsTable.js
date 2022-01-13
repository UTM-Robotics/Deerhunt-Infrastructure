import React, { useEffect } from "react";
import {
  Heading,
  Stack,
  Text,
  IconButton,
  Tooltip,
  UnorderedList,
  ListItem,
  Center,
  useDisclosure,
} from "@chakra-ui/react";
import { FaEdit } from "react-icons/fa";
import axios from "../config/config.js";
import EditTeamModal from "./EditTeamModal.js";

const TeamsTable = (props) => {
  const { isOpen, onOpen, onClose } = useDisclosure();

  useEffect(() => {
    axios
      .get("/api/teams", { params: { name: props.event } })
      .then((response) => {
        props.setTeamsData(response.data);
      });
  }, []);
  console.log(props.teamsData);
  return (
    <Center>
      <Stack m={4}>
        <Heading fontSize={{ base: "xl", sm: "2xl", md: "3xl" }}>
          Current Team{" "}
          <Tooltip label="Edit team">
            <IconButton icon={<FaEdit />} onClick={onOpen} />
          </Tooltip>
          <EditTeamModal
            isOpen={isOpen}
            onClose={onClose}
            teamsData={props.teamsData}
            setTeamsData={props.setTeamsData}
          />
        </Heading>
        <Heading fontSize={{ base: "lg", sm: "xl", md: "2xl" }}>Name</Heading>
        <Text>{props.teamsData.name}</Text>
        <Heading fontSize={{ base: "lg", sm: "xl", md: "2xl" }}>Owner</Heading>
        <Text>{props.teamsData.owner}</Text>
        <Heading fontSize={{ base: "lg", sm: "xl", md: "2xl" }}>
          Members
        </Heading>
        <UnorderedList>
          {props.teamsData.members ? (
            props.teamsData.members.map((member) => (
              <ListItem key={member}>{member}</ListItem>
            ))
          ) : (
            <p>No members</p>
          )}
        </UnorderedList>
        <Text>{ props.teamsData.last_submission_timestamp ?  "Last Submission: "+props.teamsData.last_submission_timestamp.$date: "No submission made. Please try again with a zip file." }</Text>
        <Text>{ props.teamsData.last_challenge_timestamp ?  "Last Challenge: "+props.teamsData.last_challenge_timestamp: "No challenges made." }</Text>

      </Stack>
    </Center>
  );
};

export default TeamsTable;
