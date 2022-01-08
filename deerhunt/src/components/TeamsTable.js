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

  useEffect(() => {
    axios
      .get("/api/teams", { params: { game: props.event } })
      .then((response) => {
        props.setTeamsData(response.data);
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
            teamsData={props.teamsData}
            setTeamsData={props.setTeamsData}
          />
        </Heading>
        <Heading size={"lg"}>Name</Heading>
        <Text>{props.teamsData.name}</Text>
        <Heading size={"lg"}>Owner</Heading>
        <Text>{props.teamsData.owner}</Text>
        <Heading size={"lg"}>Members</Heading>
        <UnorderedList>
          {props.teamsData.members ? props.teamsData.members.map((member) => (
            <ListItem key={member}>{member}</ListItem>
          )): <p>No members</p>
          }
        </UnorderedList>
      </Stack>
    </Center>
  );
};

export default TeamsTable;
