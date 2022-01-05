import React, { useState, useEffect } from "react";
import { Heading, Stack, Text, IconButton, Tooltip } from "@chakra-ui/react";
import { FaEdit } from "react-icons/fa";
import axios from "../config/config.js";

const mockTeamsData = [
  {
    team: "Team A",
    owner: "Joe@mail.utoronto.ca",
    members: [
      "Kat@mail.utoronto.ca",
      "Diane@mail.utoronto.ca",
      "Brandon@mail.utoronto.ca",
    ],
  },
];

const TeamsTable = () => {
  const [teamsData, setTeamsData] = useState([]);

  useEffect(() => {
    axios.get("/api/teams").then((response) => {
      setTeamsData(response.data);
      console.log(response.data);
    });
  }, []);

  return (
    <Stack m={4}>
      <Heading>
        Current Team:{" "}
        <Tooltip label="Edit team">
          <IconButton icon={<FaEdit />} />
        </Tooltip>
      </Heading>
      <Heading size={"lg"}>Owner</Heading>
      <Text>Test</Text>
      <Heading size={"lg"}>Members</Heading>
      <Text>Test</Text>
    </Stack>
  );
};

export default TeamsTable;
