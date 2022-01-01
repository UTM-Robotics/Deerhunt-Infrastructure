import React from "react";
import {
  Box,
  Heading,
  Text,
  Stack,
  Avatar,
  useColorModeValue,
  Image,
} from "@chakra-ui/react";
import BattleCodeLogo from "../images/ComingSoonLogo.png";
import MCSSLogo from "../images/MCSSLogo.png";
import UTMRoboticsLogo from "../images/UTMRoboticsLogo.png";
import CountDownTimer from "./Countdown";
import { Link } from "react-router-dom";

export default function EventList() {
  const eventsData = [
    {
      name: "Merlin",
      description:
        "Get excited for this year's Battlecode game! Program an AI that'll defend your army of knights, archers and workers while capturing a merlin to score points. Get your teams ready, this is sure to be a fun one!",
      startDate: "01/05/2022",
    },
  ];
  return eventsData.map((eventItem) => (
    <Link to={`/events/${eventItem.name}`}>
      <Box m={[8, 8, 8, 8]}>
        <Box
          maxW={"310px"}
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
            <CountDownTimer date={eventItem.startDate} />
            <Heading
              color={useColorModeValue("gray.700", "white")}
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
              <Text fontWeight={600}>Hosted by</Text>
              <Text color={"gray.500"}>UTM Robotics and MCSS</Text>
            </Stack>
          </Stack>
        </Box>
      </Box>
    </Link>
  ));
}
