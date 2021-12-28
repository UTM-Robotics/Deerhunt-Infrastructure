import React from "react";
import { useForm } from "react-hook-form";
import {
  Flex,
  Box,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Button,
} from "@chakra-ui/react";
import axios from "axios";

export default function ResetPasswordForm() {
  const {
    handleSubmit,
    register,
    formState: { isSubmitting },
  } = useForm();

  async function ResetPassword(values) {
    var form = new FormData();
    form.append("email", values.email);
    await axios
      .post("http://127.0.0.1:5000/api/user/forgotpassword", form)
      .then((response) => {
        console.log(response);
      })
      .catch(() => {
        console.log("Failed to reset password");
      });
  }

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
            <Heading size="md">Reset Password</Heading>
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
        </Box>
      </Box>
    </Flex>
  );
}
