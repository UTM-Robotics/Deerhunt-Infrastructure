import {
  Box,
  Heading,
  Text,
  Stack,
  Button,
  Grid,
  GridItem,
} from "@chakra-ui/react";
import React from "react";

const MatchCard = () => {
  const mockData = [
    {
      match_id: "001",
      time: "12:00",
      winner: "Team A",
      loser: "Team B",
    },
    {
      match_id: "002",
      time: "12:00",
      winner: "Team A",
      loser: "Team B",
    },
    {
      match_id: "002",
      time: "12:00",
      winner: "Team A",
      loser: "Team B",
    },
    {
      match_id: "002",
      time: "12:00",
      winner: "Team A",
      loser: "Team B",
    },
    {
      match_id: "002",
      time: "12:00",
      winner: "Team A",
      loser: "Team B",
    },
    {
      match_id: "002",
      time: "12:00",
      winner: "Team A",
      loser: "Team B",
    },
  ];
  return (
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
      {mockData.map((match) => (
        <GridItem>
          <Box>
            <Box
              w={"full"}
              boxShadow={"2xl"}
              rounded={"md"}
              p={6}
              overflow={"hidden"}
              bg={"white"}
            >
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
              <Stack mt={3} direction={"column"} spacing={2} align={"left"}>
                <Text color={"gray.600"} fontWeight={600}>
                  Requested by: {match.winner}
                </Text>
              </Stack>
              <Stack mt={5} direction={"row"} justifyContent={"space-between"}>
                <Button colorScheme={"orange"}>Download</Button>
                <Stack direction={"column"}>
                  <Text color={"gray.600"} fontWeight={600}>
                    Time: {match.time}
                  </Text>
                  <Text color={"gray.600"} fontWeight={600}>
                    Match ID: {match.match_id}
                  </Text>
                </Stack>
              </Stack>
            </Box>
          </Box>
        </GridItem>
      ))}
    </Grid>
  );
};

export default MatchCard;
