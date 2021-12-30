import React from "react";
import { FaEllipsisV } from "react-icons/fa";
import {
  Box,
  Heading,
  VStack,
  Text,
  IconButton,
  Tooltip,
  Table,
  Thead,
  Tr,
  Th,
  Td,
  Tbody,
} from "@chakra-ui/react";
import TopNav from "./TopNav";

export default function MyTeamsTable() {
  return (
    <Box>
      <TopNav />
      <Heading size="md" m={[4, 4, 4, 4]}>
        My Teams
      </Heading>
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Event name</Th>
            <Th>Team name </Th>
            <Th>Team owner</Th>
            <Th>Team members</Th>
            <Th />
          </Tr>
        </Thead>
        <Tbody>
          <Tr>
            <Td>Battlecode</Td>
            <Td>Team A</Td>
            <Td>Joe</Td>
            <Td>
              <VStack alignItems={"left"}>
                <Text>Francis</Text>
                <Text>Barbara</Text>
                <Text>Kiki</Text>
              </VStack>
            </Td>
            <Td>
              <Tooltip label="Edit team">
                <IconButton icon={<FaEllipsisV />}></IconButton>
              </Tooltip>
            </Td>
          </Tr>
        </Tbody>
      </Table>
    </Box>
  );
}
