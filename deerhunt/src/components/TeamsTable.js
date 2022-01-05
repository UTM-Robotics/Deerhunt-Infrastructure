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
} from "@chakra-ui/react";
import { FaEdit } from "react-icons/fa";
import axios from "../config/config.js";

const TeamsTable = () => {
  const [teamsData, setTeamsData] = useState([]);
  const [membersList, setMembersList] = useState([]);

  useEffect(() => {
    axios.get("/api/teams").then((response) => {
      setTeamsData(response.data[0]);
      setMembersList(response.data[0].members);
    });
  }, []);

  return (
    <Center>
      <Stack m={4}>
        <Heading>
          Current Team{" "}
          <Tooltip label="Edit team">
            <IconButton icon={<FaEdit />} />
          </Tooltip>
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
