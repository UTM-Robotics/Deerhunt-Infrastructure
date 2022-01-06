import React from "react";
import { IconButton, Flex, useColorMode, Box } from "@chakra-ui/react";
import { FaMoon } from "react-icons/fa";

const ColourModeToggle = () => {
  const { colorMode, toggleColorMode } = useColorMode();

  return (
    <Box position="fixed" bottom={0} right={0}>
      <IconButton icon={<FaMoon />} onClick={() => toggleColorMode()}>
        Toggle Mode {colorMode}
      </IconButton>
    </Box>
  );
};

export default ColourModeToggle;
