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
  InputRightElement, ListItem, UnorderedList,
} from "@chakra-ui/react";
import {useForm} from "react-hook-form";
import axios from "../config/config";

const EditTeamModal = (props) => {
  const {
    handleSubmit,
    register,
    formState: { isSubmitting },
  } = useForm();

  async function AddMembers(values) {
    let form = new FormData();
    form.append("email", values.email);
    form.append("name", props.teamsData.name);
    await axios
        .post("/api/addmember", form)
        .then((response) => {
          console.log(response.data);
          console.log("Successfully added user");
          props.setTeamsData(response.data);
          props.onClose();
        })
        .catch(() => {});
  }

  return (
    <>
      <Modal isOpen={props.isOpen} onClose={props.onClose}>
        <ModalOverlay>
          <ModalContent>
            <ModalHeader>Edit Team</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              <Text fontWeight={700}>{"Team name: "}</Text>
              <Text>{props.teamsData.name}</Text>
              <Text fontWeight={700}>{"Team owner: "}</Text>
              <Text>{props.teamsData.owner}</Text>
              <Text fontWeight={700}>Team members:</Text>
              <UnorderedList>
                {props.teamsData.members ? props.teamsData.members.map((member) => (
                    <ListItem key={member}>{member}</ListItem>
                )): <p>No members</p>
                }
              </UnorderedList>

              <form onSubmit={handleSubmit(AddMembers)}>
              <InputGroup mt={3}>
                <Input
                  type="text"
                  placeholder="Enter member's email"
                   {...register("email", {
                     required: "This is required",
                   })}
                />
                <InputRightElement width="4.5rem">
                  <Button h="1.75rem" fontSize={"sm"} colorScheme={"green"} isLoading={isSubmitting} type="submit">
                    Add
                  </Button>
                </InputRightElement>
              </InputGroup>
              </form>
            </ModalBody>
            <ModalFooter>
              <Button mr={3} colorScheme={"red"} >
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
