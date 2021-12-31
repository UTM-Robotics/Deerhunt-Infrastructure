import React from "react";
import {
  Heading,
  Tabs,
  TabList,
  Tab,
  TabPanels,
  TabPanel,
} from "@chakra-ui/react";
import TopNav from "../components/TopNav";
import TeamsPanel from "../components/TeamsPanel";

const EventUserPage = () => {
  return (
    <>
      <TopNav />
      <Heading size="md" m={[4, 4, 4, 4]}>
        Some Event
      </Heading>
      <Tabs isFitted variant="enclosed-colored">
        <TabList>
          <Tab>Event Details</Tab>
          <Tab>Tutorial</Tab>
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
            <TeamsPanel />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </>
  );
};

export default EventUserPage;
