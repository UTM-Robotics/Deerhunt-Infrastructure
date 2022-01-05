import React, { useEffect, useState } from "react";
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
import axios from "../config/config.js";

const Leaderboard = (props) => {
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    axios
      .get("/api/leaderboard", {
        params: { name: props.event },
      })
      .then((response) => {
        setLeaderboard(response.data);
        console.log(response.data);
      });
  }, []);

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
        {leaderboard.map((team, index) => (
          <Tr key={index}>
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
