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
import ChangePasswordPage from "../pages/ChangePasswordPage";

export default function ChangePasswordForm() {
  const [error, setError] = useState(null);

  const {
    handleSubmit,
    register,
    formState: { isSubmitting },
  } = useForm();

  async function ChangePassword(values) {
    var form = new FormData();
    form.append("old_password", values.old_password);
    form.append("new_password", values.new_password);
    await axios
      .post("api/user/changepassword", form)
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
        Success! Your password has been changed
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
              Change Password
            </Heading>
            
          </Box>
          <Box>
            <form onSubmit={handleSubmit(ChangePassword)}>
              <FormControl>
                <FormLabel>Old Password</FormLabel>
                <Input
                  type="password"
                  placeholder="Enter Your old password"
                  {...register("old_password", {
                    required: "This is required",
                  })}
                />
              </FormControl>
             
              <FormControl>
                <FormLabel>New Password</FormLabel>
                <Input
                  type="password"
                  placeholder="Enter Your new password"
                  {...register("new_password", {
                    required: "This is required",
                    minLength: {
                        value: 8,
                        message: "Minimum length should be 8",
                      },
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
