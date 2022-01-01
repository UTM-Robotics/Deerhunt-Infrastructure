import React from "react";
import { useDropzone } from "react-dropzone";
import {
  Heading,
  Text,
  Box,
  UnorderedList,
  ListItem,
  Input,
  VStack,
} from "@chakra-ui/react";

function SubmissionForm() {
  const { acceptedFiles, getRootProps, getInputProps } = useDropzone();

  const files = acceptedFiles.map((file) => (
    <ListItem key={file.path}>{file.path}</ListItem>
  ));

  let formData = new FormData();

  const fileObjects = acceptedFiles.map((file) => {
    console.log(file);
    formData.append("assets", file, file.name);
  });

  return (
    <VStack m={6}>
      <Heading size={"lg"}>Submission</Heading>
      <Box
        borderWidth={3}
        borderRadius={"lg"}
        _hover={{ background: "gray.200" }}
        {...getRootProps()}
      >
        <Input {...getInputProps()} />
        <Text p={[10, 10, 10, 10]}>
          Drag and drop your files or click to select a file
        </Text>
      </Box>
      <Heading size={"md"}>File:</Heading>
      <UnorderedList>{files}</UnorderedList>
    </VStack>
  );
}

export default SubmissionForm;
