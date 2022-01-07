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
        console.log(response.data);
        console.log(props.event);
      });
  }, []);

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
            teamsData={teamsData}
          />
        </Heading>
        <Heading fontSize={{ base: "lg", sm: "xl", md: "2xl" }}>Name</Heading>
        <Text>{teamsData.name}</Text>
        <Heading fontSize={{ base: "lg", sm: "xl", md: "2xl" }}>Owner</Heading>
        <Text>{teamsData.owner}</Text>
        <Heading fontSize={{ base: "lg", sm: "xl", md: "2xl" }}>
          Members
        </Heading>
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
