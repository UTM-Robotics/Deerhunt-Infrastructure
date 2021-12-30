import React, { useState } from "react";
import { useForm } from "react-hook-form";
import {
  Flex,
  Box,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Button,
  Text,
  Alert,
  AlertIcon,
} from "@chakra-ui/react";
import axios from "../config/config";

export default function ResetPasswordForm() {
  const [error, setError] = useState(null);

  const {
    handleSubmit,
    register,
    formState: { isSubmitting },
  } = useForm();

  async function ResetPassword(values) {
    var form = new FormData();
    form.append("email", values.email);
    await axios
      .post("api/user/forgotpassword", form)
      .then((response) => {
        setError("Success");
      })
      .catch(() => {
        /*Failed to reset password*/
        setError("Error");
      });
  }

  const ErrorMessage = () => {
    return (
      <Alert status="error">
        <AlertIcon />
        There was an error processing your request
      </Alert>
    );
  };

  const SuccessMessage = () => {
    return (
      <Alert status="success">
        <AlertIcon />
        Success! Check your email for the password reset link
      </Alert>
    );
  };

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
            <Heading size="md" mb={4}>
              Reset Password
            </Heading>
            <Text>Enter the email associated with your account</Text>
          </Box>
          <Box>
            <form onSubmit={handleSubmit(ResetPassword)}>
              <FormControl>
                <FormLabel>Email</FormLabel>
                <Input
                  type="email"
                  placeholder="Enter Your Email"
                  {...register("email", {
                    required: "This is required",
                  })}
                />
              </FormControl>
              <Box my={4}>
                <Button width="full" isLoading={isSubmitting} type="submit">
                  Submit
                </Button>
              </Box>
            </form>
          </Box>
          {error === "Success" ? SuccessMessage() : null}
          {error === "Error" ? ErrorMessage() : null}
        </Box>
      </Box>
    </Flex>
  );
}
