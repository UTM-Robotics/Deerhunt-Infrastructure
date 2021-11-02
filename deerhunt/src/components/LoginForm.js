import React from "react";
import {
  Flex,
  Box,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Button,
} from "@chakra-ui/react";

const LoginForm = () => {
  return (
    <Flex
      minHeight="100vh"
      width="full"
      justifyContent="center"
      alignItems="center"
    >
      <Box>
        <Box
          borderWidth={1}
          px={6}
          py={6}
          borderRadius={4}
          boxShadow="lg"
          width="full"
          maxWidth="500px"
          bg="gray.300"
        >
          <Box textAlign="center" mb={4}>
            <Heading>Login to Deerhunt</Heading>
          </Box>
          <Box>
            <form>
              <FormControl>
                <FormLabel>Email</FormLabel>
                <Input type="email" placeholder="Enter Your Email" />
              </FormControl>
              <FormControl mt={4}>
                <FormLabel>Password</FormLabel>
                <Input type="password" placeholder="Enter Your Password" />
              </FormControl>
              <Box my={4}>
                <Button width="full">Login</Button>
              </Box>
              <Box my={4}>
                <Button width="full">Create An Account</Button>
              </Box>
            </form>
          </Box>
        </Box>
      </Box>
    </Flex>
  );
};

export default LoginForm;
