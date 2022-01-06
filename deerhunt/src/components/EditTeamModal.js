import React from "react";
import {
  Modal,
  ModalContent,
  ModalOverlay,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  Button,
  Text,
  List,
  ListItem,
  InputGroup,
  Input,
  InputRightElement,
} from "@chakra-ui/react";

const EditTeamModal = (props) => {
  return (
    <>
      <Modal isOpen={props.isOpen} onClose={props.isClose}>
        <ModalOverlay>
          <ModalContent>
            <ModalHeader>Edit Team</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              <Text fontWeight={700}>{"Team name: "}</Text>
              <Text>{props.teamsData[0].team}</Text>
              <Text fontWeight={700}>{"Team owner: "}</Text>
              <Text>{props.teamsData[0].owner}</Text>
              <Text fontWeight={700}>Team members:</Text>
              <List>
                {props.teamsData[0].members.map((member, index) => (
                  <ListItem key={index}>{member}</ListItem>
                ))}
              </List>
              <InputGroup mt={3}>
                <Input placeholder="Enter member's email" />
                <InputRightElement width="4.5rem">
                  <Button h="1.75rem" fontSize={"sm"} colorScheme={"green"}>
                    Add
                  </Button>
                </InputRightElement>
              </InputGroup>
            </ModalBody>
            <ModalFooter>
              <Button mr={3} colorScheme={"red"}>
                Leave team
              </Button>
            </ModalFooter>
          </ModalContent>
        </ModalOverlay>
      </Modal>
    </>
  );
};

export default EditTeamModal;
