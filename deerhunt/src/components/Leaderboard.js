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
  AlertIcon,
  Alert,
  AlertDescription,
  CloseButton,
} from "@chakra-ui/react";
import axios from "../config/config.js";

const Leaderboard = (props) => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [myTeam, setMyTeam] = useState("");

  useEffect(() => {
    axios
      .get("/api/teams", { params: { game: props.event } })
      .then((response) => {
        setMyTeam(response.data);
      });
    axios
      .get("/api/leaderboard", {
        params: { name: props.event },
      })
      .then((response) => {
        setLeaderboard(response.data);
      });
  }, []);

  const getChallengeFunction = (team, opponent) => {
    return () => {
      var form = new FormData();
      form.append("name", props.event);
      form.append("team1_id", team._id);
      form.append("team2_id", opponent._id);
      axios
        .post("/api/requests", form)
        .then((response) => console.log(response));
    };
  };

  const InvalidChallenge = () => {
    return (
      <Alert>
        <AlertIcon />
        <AlertDescription>Cannot challenge your own team!</AlertDescription>
        <CloseButton position="absolute" right={4} top={4} />
      </Alert>
    );
  };

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
              <Button
                onClick={
                  myTeam._id !== team._id ? (
                    getChallengeFunction(myTeam, team)
                  ) : (
                    <InvalidChallenge />
                  )
                }
              >
                Challenge
              </Button>
            </Td>
          </Tr>
        ))}
      </Tbody>
    </Table>
  );
};

export default Leaderboard;
