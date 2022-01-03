import React from "react";
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableCaption,
  Button,
} from "@chakra-ui/react";

const Leaderboard = () => {
  const mockData = [
    {
      name: "Team A",
    },
    {
      name: "Team B",
    },
    {
      name: "Team C",
    },
  ];
  return (
    <Table>
      <TableCaption>
        Press challenge to play a team and overtake them on the leaderboard!
      </TableCaption>
      <Thead>
        <Tr>
          <Th>#</Th>
          <Th>Team</Th>
          <Th />
        </Tr>
      </Thead>
      <Tbody>
        {mockData.map((team, index) => (
          <Tr>
            <Td>{index + 1}</Td>
            <Td>{team.name}</Td>
            <Td>
              <Button>Challenge</Button>
            </Td>
          </Tr>
        ))}
      </Tbody>
    </Table>
  );
};

export default Leaderboard;
