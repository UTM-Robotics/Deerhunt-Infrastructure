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
  FormHelperText,
} from "@chakra-ui/react";
import React, { useState } from "react";
import { useForm } from "react-hook-form";
import axios from "../config/config";
import FeedbackAlert from "./FeedbackAlert";

const CreateTeam = (props) => {
  const [feedback, setFeedback] = useState("");
  const [feedbackMessage, setFeedbackMessage] = useState("");
  const {
    handleSubmit,
    register,
    formState: { isSubmitting },
  } = useForm();

  async function CreateTeam(values) {
    let form = new FormData();
    form.append("name", values.name);
    form.append("event_name", props.event);
    await axios
      .post("api/teams", form)
      .then((response) => {
        setFeedback("success");
        setFeedbackMessage(response.data.message);
      })
      .catch((error) => {
        setFeedback("error");
        if (error.response) {
          if (error.response.data) {
            setFeedbackMessage(error.response.data);
          } else {
            setFeedbackMessage("Unknown error, please try again!");
          }
        } else {
          setFeedbackMessage("Could not reach server, please try again!");
        }
      });
  }
  return (
    <>
      <Modal isOpen={props.isOpen} onClose={props.onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Create a New Team</ModalHeader>
          <ModalCloseButton />

          <form onSubmit={handleSubmit(CreateTeam)}>
            <ModalBody>
              <FormControl>
                <FormLabel>Team Name</FormLabel>
                <Input
                  type="text"
                  placeholder="Enter a team name"
                  {...register("name", {
                    required: "This is required",
                  })}
                />
                <FormHelperText>
                  Team names may consist of letters, numbers and underscores
                </FormHelperText>
              </FormControl>
            </ModalBody>
            <ModalFooter>
              <Button isLoading={isSubmitting} type="submit">
                Create Team
              </Button>
            </ModalFooter>
          </form>
          {feedback === "success" ? (
            <FeedbackAlert status={feedback} description={feedbackMessage} />
          ) : null}
          {feedback === "error" ? (
            <FeedbackAlert status={feedback} description={feedbackMessage} />
          ) : null}
        </ModalContent>
      </Modal>
    </>
  );
};

export default CreateTeam;
