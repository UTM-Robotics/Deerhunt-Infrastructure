import React, { useState, useEffect } from "react";
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
import AddTeamModal from "./AddTeamModal.js";
import EditTeamModal from "./EditTeamModal.js";

const TeamsTable = (props) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [teamsData, setTeamsData] = useState([]);
  const [membersList, setMembersList] = useState([]);

  useEffect(() => {
    axios
      .get("/api/teams", { params: { game: props.event } })
      .then((response) => {
        setTeamsData(response.data);
        setMembersList(response.data.members);
      });
  }, []);

  return (
    <Center>
      <Stack m={4}>
        <Heading>
          Current Team{" "}
          <Tooltip label="Edit team">
            <IconButton icon={<FaEdit />} onClick={onOpen} />
          </Tooltip>
          <EditTeamModal
            isOpen={isOpen}
            onClose={onClose}
            teamsData={teamsData}
          />
        </Heading>
        <Heading size={"lg"}>Name</Heading>
        <Text>{teamsData.name}</Text>
        <Heading size={"lg"}>Owner</Heading>
        <Text>{teamsData.owner}</Text>
        <Heading size={"lg"}>Members</Heading>
        <UnorderedList>
          {membersList.map((member) => (
            <ListItem>{member}</ListItem>
          ))}
        </UnorderedList>
      </Stack>
    </Center>
  );
};

export default TeamsTable;
