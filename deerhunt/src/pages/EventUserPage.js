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
import TopNav from "../components/TopNav";
import TeamsPanel from "../components/TeamsPanel";
import { useParams } from "react-router-dom";
import Leaderboard from "../components/Leaderboard";

const EventUserPage = () => {
  let { event } = useParams();
  console.log(event);
  return (
    <>
      <TopNav />
      <Center>
        <Heading size="lg" m={[4, 4, 4, 4]}>
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
            <p>Test</p>
          </TabPanel>
          <TabPanel>
            <p>Test</p>
          </TabPanel>
          <TabPanel>
            <Leaderboard />
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
