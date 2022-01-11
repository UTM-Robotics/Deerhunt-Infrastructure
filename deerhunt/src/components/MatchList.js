import {
  Box,
  Heading,
  Text,
  Stack,
  Button,
  Grid,
  GridItem,
  Center,
} from "@chakra-ui/react";
import React, { useState, useEffect } from "react";
import axios from "../config/config.js";

const MatchList = (props) => {
  const [matches, setMatches] = useState([]);
  const mockData = [
    {
      match_id: "001",
      time: "12:00",
      winner: "Team A",
      loser: "Team B",
    },
  ];
  let DownloadMatch = (match) => { 
    return () => { 
      axios.get("/api/match/download", {params:{match_id: match._id}}).then((response) => {
      }).catch((e)=>{console.log(e);});
    };
  
  };
  useEffect(() => {
    axios
      .get("/api/match", { params: { event_name: props.event } })
      .then((response) => {
        setMatches(response.data);
        console.log(response.data);
      });
  }, []);

  return (
    <>
      <Heading fontSize={{ base: "xl", sm: "2xl", md: "3xl" }}>
        Match History
      </Heading>
      <Grid
        templateColumns={{
          base: "repeat(1, 1fr)",
          sm: "repeat(2, 1fr)",
          md: "repeat(3, 1fr)",
          lg: "repeat(4, 1fr)",
        }}
        gap={6}
        m={6}
      >
        {matches.map((match, index) => (
          <GridItem key={index}>
            <Box>
              <Box
                w={"full"}
                boxShadow={"2xl"}
                rounded={"md"}
                p={6}
                overflow={"hidden"}
                bg={"white"}
              >
                <Center>
                  <div>
                    <Stack direction={"row"} spacing={{ base: 1, md: 2 }}>
                      <Heading
                        color="green.600"
                        fontSize={{ base: "lg", sm: "xl", md: "2xl" }}
                      >
                        {match.winner}
                      </Heading>
                      <Heading
                        color="gray.700"
                        fontSize={{ base: "lg", sm: "xl", md: "2xl" }}
                      >
                        vs.{" "}
                      </Heading>
                      <Heading
                        color="red.600"
                        fontSize={{ base: "lg", sm: "xl", md: "2xl" }}
                      >
                        {match.loser}
                      </Heading>
                    </Stack>
                    <Stack>
                      <Text color={"gray.700"}>Match ID: {match.match_id}</Text>
                      <Button colorScheme={"orange"} onClick={DownloadMatch(match)}>Download</Button>
                    </Stack>
                  </div>
                </Center>
              </Box>
            </Box>
          </GridItem>
        ))}
      </Grid>
    </>
  );
};

export default MatchList;
