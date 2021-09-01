import React from "react"
import { Box, Button, HStack } from "@chakra-ui/react"
 
export default function Navbar(props) {
  return (
    <Box bg="green" w="100%" p={3}>
      <HStack>
        <Button>
          Home
        </Button>
      </HStack>
    </Box>
  )
}