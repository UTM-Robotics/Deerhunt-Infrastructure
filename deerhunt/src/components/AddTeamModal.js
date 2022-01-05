import {
  ModalCloseButton,
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  ModalOverlay,
  Button,
  FormControl,
  FormLabel,
  Input,
} from "@chakra-ui/react";
import React from "react";
import { useForm } from "react-hook-form";
import axios from "../config/config";

const CreateTeam = (props) => {
  const {
    handleSubmit,
    register,
    formState: { isSubmitting },
  } = useForm();

  async function CreateTeam(values) {
    var form = new FormData();
    form.append("name", values.name);
    form.append("event_name", props.event);
    await axios
      .post("api/teams", form)
      .then((response) => {
        console.log(response);
      })
      .catch(() => {});
  }
  return (
    <>
      <Modal isOpen={props.isOpen} onClose={props.onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Create a New Team</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <form onSubmit={handleSubmit(CreateTeam)}>
              <FormControl>
                <FormLabel>Team Name</FormLabel>
                <Input
                  type="text"
                  placeholder="Enter a team name"
                  {...register("name", {
                    required: "This is required",
                  })}
                />
              </FormControl>
            </form>
          </ModalBody>
          <ModalFooter>
            <Button isLoading={isSubmitting} type="submit">
              Create Team
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
};

export default CreateTeam;
