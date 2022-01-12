import {
  Box,
  Heading,
  Text,
  Stack,
  Button,
  Link,
  Grid,
  GridItem,
  Center,
} from "@chakra-ui/react";
import React, { useState, useEffect } from "react";
import axios from "../config/config.js";

const MatchList = (props) => {
  const [matches, setMatches] = useState([]);

  let DownloadMatch = (match) => {
    return () => {
      axios
        .get("/api/match/download", { params: { match_id: match._id } })
        .then((response) => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", "match" + match._id + ".zip");
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        })
        .catch((e) => {
          console.log(e);
        });
    };
  };
  useEffect(() => {
    axios
      .get("/api/match", { params: { event_name: props.event } })
      .then((response) => {
        setMatches(response.data);
        console.log("Data params");
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
                    <Stack direction={"column"} spacing={{ base: 1, md: 2 }}>
                      <Heading
                        color="green.600"
                        fontSize={{ base: "md", sm: "lg", md: "xl" }}
                      >
                        {match.winner.length > 20
                          ? match.winner.substring(0, 21) + "..."
                          : match.winner}
                      </Heading>
                      <Heading
                        color="gray.700"
                        fontSize={{ base: "md", sm: "lg", md: "xl" }}
                      >
                        vs.{" "}
                      </Heading>
                      <Heading
                        color="red.600"
                        fontSize={{ base: "md", sm: "lg", md: "xl" }}
                      >
                        {match.loser.length > 20
                          ? match.loser.substring(0, 21) + "..."
                          : match.loser}
                      </Heading>
                    </Stack>
                    <Stack m={3}>
                      <Text color={"gray.700"}>Match ID: {match._id}</Text>
                      {/* <Button
                        colorScheme={"orange"}
                        onClick={DownloadMatch(match)}
                      >
                        Download
                      </Button> */}

                    <Link href={'https://mcss.utmrobotics.com/api/match/download?'+match._id} color={"red.700"} isExternal>
                        Download Match
                    </Link>
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
