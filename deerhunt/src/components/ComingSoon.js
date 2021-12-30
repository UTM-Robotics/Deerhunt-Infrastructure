import React from "react";
import { Flex, Box, Heading, Button, Link, Text } from "@chakra-ui/react";
import history from "../history";

export default function ComingSoon() {
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
          px={8}
          py={8}
          borderRadius={4}
          boxShadow="lg"
          width="full"
          maxWidth="500px"
          bg="gray.300"
        >
          <Box textAlign="center" mb={4}>
            <Heading size="lg" m={[4, 4, 4, 4]}>
              Coming soon!
            </Heading>
            <Text>Check our Discord to learn more about upcoming events.</Text>
            <Link
              onClick={() => {
                history.replace("/");
              }}
            >
              <Box my={8}>
                <Button width="full">Back to Home</Button>
              </Box>
            </Link>
          </Box>
        </Box>
      </Box>
    </Flex>
  );
}
