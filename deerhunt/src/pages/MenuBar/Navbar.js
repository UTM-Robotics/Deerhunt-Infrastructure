import React from "react"
import history from '../../history'
import { Box, Button, HStack } from "@chakra-ui/react"
 
export default function Navbar(props) {
  return (
    <Box bg="green" w="100%" p={3}>
      <HStack>
        <Button onClick={()=> history.push('/')}>
          Home
        </Button>
        <Button onClick={()=> history.push('/login')}>
          Sign in
        </Button>
        <Button onClick={()=> history.push('/signup')}>
          Sign up
        </Button>
      </HStack>
    </Box>
  )
}