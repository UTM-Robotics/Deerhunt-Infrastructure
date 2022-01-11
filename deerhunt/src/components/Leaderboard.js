import React, { useEffect, useState } from "react";
import {
  Text,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableCaption,
  Button,
  Center
} from "@chakra-ui/react";
import axios from "../config/config.js";

const Leaderboard = (props) => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [myTeam, setMyTeam] = useState("");
  const [challengeMessage, setChallengeMessage] = useState("");
  useEffect(() => {
    let form = new FormData();
    form.append("name", props.event);
    axios
      .post("/api/user/team", form)
      .then((response) => {
        setMyTeam(response.data);
      })
      .catch((e) => {
        console.log(e);
      });
    axios
      .get("/api/leaderboard", {
        params: { name: props.event },
      })
      .then((response) => {
        setLeaderboard(response.data);
      })
      .catch((e) => {
        console.log(e);
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
        .then((response) => setChallengeMessage(response.data.message))
        .catch((error)=>{
          if (error.response) {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
          }

        }
        );
    };
  };
  return (
    <>
    <Center>
       <Text>See recent matches on the Team tab.</Text>
    </Center>
    <Table>
      <TableCaption>
        {leaderboard.length == 0?"Press challenge to play a team and overtake them on the leaderboard!": "Please log in to see the leaderboard!"}
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
              {index < leaderboard.map((e) => e.name).indexOf(myTeam.name) ? (
                <Button onClick={getChallengeFunction(myTeam, team)}>
                  Challenge
                </Button>
              ) : null}
            </Td>
          </Tr>
        ))}
      </Tbody>
    </Table>
    </>
  );
};

export default Leaderboard;
