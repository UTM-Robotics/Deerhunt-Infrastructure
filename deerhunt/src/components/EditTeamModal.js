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
  InputGroup,
  Input,
  InputRightElement,
} from "@chakra-ui/react";

const EditTeamModal = (props) => {
  return (
    <>
      <Modal isOpen={props.isOpen} onClose={props.onClose}>
        <ModalOverlay>
          <ModalContent>
            <ModalHeader>Edit Team</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              <Text fontWeight={700}>{"Team name: "}</Text>
              <Text></Text>
              <Text fontWeight={700}>{"Team owner: "}</Text>
              <Text></Text>
              <Text fontWeight={700}>Team members:</Text>

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
