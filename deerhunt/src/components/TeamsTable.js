import React, { useState } from "react";
import { FaEllipsisV } from "react-icons/fa";
import {
  VStack,
  Text,
  IconButton,
  Tooltip,
  Tr,
  Td,
  Tbody,
  Table,
  Thead,
  Th,
  useDisclosure,
} from "@chakra-ui/react";
import EditTeamModal from "./EditTeamModal";

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
  const [teamsData, setTeamsData] = useState(mockTeamsData);
  const { isOpen, onOpen, onClose } = useDisclosure();
  return (
    <Table variant="simple" size={"md"}>
      <Thead>
        <Tr>
          <Th>Team name </Th>
          <Th>Team owner</Th>
          <Th>Team members</Th>
          <Th />
        </Tr>
      </Thead>
      <Tbody>
        {teamsData.map((team, index) => (
          <Tr key={index}>
            <Td>{team.team}</Td>
            <Td>{team.owner}</Td>
            <Td>
              <VStack alignItems={"left"}>
                <Text>{team.members[0]}</Text>
                <Text>{team.members[1]}</Text>
                <Text>{team.members[2]}</Text>
              </VStack>
            </Td>
            <Td>
              <Tooltip label="Edit team">
                <IconButton icon={<FaEllipsisV />} onClick={onOpen} />
              </Tooltip>
              <EditTeamModal
                isOpen={isOpen}
                isClose={onClose}
                teamsData={teamsData}
              />
            </Td>
          </Tr>
        ))}
      </Tbody>
    </Table>
  );
};

export default TeamsTable;
