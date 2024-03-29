import React from "react";
import {
  Heading,
  Tabs,
  TabList,
  Tab,
  TabPanels,
  TabPanel,
  Center,
} from "@chakra-ui/react";
import TeamsPanel from "../components/TeamsPanel";
import { useParams } from "react-router-dom";
import Leaderboard from "../components/Leaderboard";
import EventDetailsPanel from "../components/EventDetailsPanel";
import TutorialPanel from "../components/TutorialPanel";

const EventUserPage = () => {
  let { event } = useParams();
  return (
    <>
      <Center>
        <Heading fontSize={{ base: "xl", sm: "2xl", md: "3xl" }} m={4}>
          {event}
        </Heading>
      </Center>
      <Tabs isFitted variant="enclosed-colored">
        <TabList>
          <Tab>Event Details</Tab>
          <Tab>Tutorial</Tab>
          <Tab>Leaderboard</Tab>
          <Tab>Team</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <EventDetailsPanel event={event} />
          </TabPanel>
          <TabPanel>
            <TutorialPanel event={event} />
          </TabPanel>
          <TabPanel>
            <Leaderboard event={event} />
          </TabPanel>
          <TabPanel>
            <TeamsPanel event={event} />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </>
  );
};

export default EventUserPage;
