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
import axios from "../config/config";

export default function LoginForm() {
  const {
    handleSubmit,
    register,
    formState: { isSubmitting },
  } = useForm();

  async function login(values) {
    var form = new FormData();
    form.append("username", values.username);
    form.append("password", values.password);
    await axios
      .post("api/admin/auth", form)
      .then((response) => {
        console.log(response);
      })
      .catch(() => {
        console.log("failed to login");
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
        >
          <Box textAlign="center" mb={4}>
            <Heading size="md">Admin Login</Heading>
          </Box>
          <Box>
            <form onSubmit={handleSubmit(login)}>
              <FormControl>
                <FormLabel>Username</FormLabel>
                <Input
                  type="text"
                  placeholder="Enter Your Username"
                  {...register("username", {
                    required: "This is required",
                  })}
                />
              </FormControl>
              <FormControl mt={4}>
                <FormLabel>Password</FormLabel>
                <Input
                  type="password"
                  placeholder="Enter Your Password"
                  {...register("password", {
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
                  Login
                </Button>
              </Box>
            </form>
          </Box>
        </Box>
      </Box>
    </Flex>
  );
}
