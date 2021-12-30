import React from "react";
import { Modal, ModalContent } from "@chakra-ui/react";
import { useDisclosure } from "@chakra-ui/react";

export default function EditTeamModal() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  return (
    <Modal isOpen={isOpen} onClose={onClose}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Edit Team</ModalHeader>
      </ModalContent>
    </Modal>
  );
}
