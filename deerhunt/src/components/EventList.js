import React, { useState, useEffect } from "react";
import {
  Box,
  Heading,
  Text,
  Stack,
  Avatar,
  Image,
  Grid,
  GridItem,
} from "@chakra-ui/react";
import BattleCodeLogo from "../images/ComingSoonLogo.png";
import MCSSLogo from "../images/MCSSLogo.png";
import UTMRoboticsLogo from "../images/UTMRoboticsLogo.png";
import CountDownTimer from "./Countdown";
import { Link } from "react-router-dom";
import axios from "../config/config.js";

export default function EventList() {
  const [eventsData, setEventsData] = useState([]);

  useEffect(() => {
    axios.get("/api/events").then((response) => {
      setEventsData(response.data);
      console.log(response.data);
    });
  }, []);

  return (
    <Grid
      templateColumns={{
        base: "repeat(1, 1fr)",
        md: "repeat(2, 1fr)",
        lg: "repeat(3, 1fr)",
      }}
      gap={6}
      m={6}
    >
      {eventsData.map((eventItem) => (
        <Link to={`/events/${eventItem.name}`}>
          {/*the above change makes it so that the links are the event names but also passes in the event name*/}
          {/*to the sub panels instead of the game name which fixes things, so we can use the controllers*/}
          <GridItem>
            <Box>
              <Box
                w={"full"}
                bg="white"
                boxShadow={"2xl"}
                rounded={"md"}
                p={6}
                overflow={"hidden"}
              >
                <Box
                  h={"100%"}
                  bg={"gray.100"}
                  mt={-6}
                  mx={-6}
                  mb={6}
                  pos={"relative"}
                >
                  <Image src={BattleCodeLogo} layout={"flex"} />
                </Box>

                <Stack>
                  <Text
                    color={"red"}
                    textTransform={"uppercase"}
                    fontWeight={800}
                    fontSize={"sm"}
                    letterSpacing={1.1}
                  >
                    Coming in:
                  </Text>
                  <CountDownTimer date={eventItem.starttime} />
                  <Heading
                    color="gray.700"
                    fontSize={"2xl"}
                    fontFamily={"body"}
                  >
                    {eventItem.name}
                  </Heading>
                  <Text color={"gray.500"} fontSize={"sm"}>
                    {eventItem.description}
                  </Text>
                </Stack>
                <Stack mt={6} direction={"row"} spacing={4} align={"center"}>
                  <Avatar bg={"transparent"}>
                    <Image src={UTMRoboticsLogo} layout={"flex"} />
                  </Avatar>
                  <Avatar bg={"transparent"}>
                    <Image src={MCSSLogo} layout={"flex"} />
                  </Avatar>
                  <Stack direction={"column"} spacing={0} fontSize={"sm"}>
                    <Text color={"gray.600"} fontWeight={600}>
                      Hosted by
                    </Text>
                    <Text color={"gray.500"}>UTM Robotics and MCSS</Text>
                  </Stack>
                </Stack>
              </Box>
            </Box>
          </GridItem>
        </Link>
      ))}
    </Grid>
  );
}
