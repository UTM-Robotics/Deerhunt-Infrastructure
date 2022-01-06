import React from "react";
import { useDropzone } from "react-dropzone";
import { useForm } from "react-hook-form";
import {
  Heading,
  Text,
  Box,
  UnorderedList,
  ListItem,
  Input,
  Button,
  FormControl,
  Center,
} from "@chakra-ui/react";

function SubmissionForm(props) {
  const { acceptedFiles, getRootProps, getInputProps } = useDropzone();
  const {
    handleSubmit,
    formState: { isSubmitting },
  } = useForm();

  const files = acceptedFiles.map((file) => (
    <ListItem key={file.path}>
      {file.path} - {file.size} bytes
    </ListItem>
  ));

  const onSubmit = (values) => {
    props.submissionCallback(acceptedFiles);
  };
  return (
    <Center>
      <Box display={"inline-block"} textAlign={"center"}>
        <Heading size={"lg"} m={4}>
          Submission
        </Heading>
        <Box alignItems={"center"}>
          <form onSubmit={handleSubmit(onSubmit)}>
            <FormControl>
              <Box
                borderWidth={3}
                borderRadius={"lg"}
                _hover={{ background: "gray.200" }}
                {...getRootProps()}
              >
                <Input {...getInputProps()} />
                <Text p={10}>
                  Drag and drop your files or click to select a file
                </Text>
              </Box>
              <Heading size={"md"} m={4}>
                File:
              </Heading>
              <UnorderedList>{files}</UnorderedList>
              <Button type="submit" isLoading={isSubmitting}>
                Submit
              </Button>
            </FormControl>
          </form>
        </Box>
      </Box>
    </Center>
  );
}

export default SubmissionForm;
