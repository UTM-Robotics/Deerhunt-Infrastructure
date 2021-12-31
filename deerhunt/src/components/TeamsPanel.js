import React from "react";
import { Box, Button, Stack, useDisclosure } from "@chakra-ui/react";

import TeamsTable from "./TeamsTable";
import AddTeamModal from "./AddTeamModal";

export default function TeamsPanel() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  return (
    <Box>
      <Box textAlign="left">
        <Button m={[4, 4, 4, 4]} onClick={onOpen}>
          Create a New Team
        </Button>
        <AddTeamModal isOpen={isOpen} onClose={onClose} />
        <TeamsTable />
      </Box>
    </Box>
  );
}
