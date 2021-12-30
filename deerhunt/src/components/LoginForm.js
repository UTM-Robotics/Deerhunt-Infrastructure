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
  Link,
  Text,
} from "@chakra-ui/react";
import axios from "../config/config";

export default function LoginForm(props) {
  const {
    handleSubmit,
    register,
    formState: {isSubmitting},
  } = useForm();

  async function login(values) {
    var form = new FormData();
    form.append("email", values.email);
    form.append("password", values.password);
    await axios
      .post("api/user/auth", form)
      .then((response) => {
        console.log(response);
        if (response.data.token) {
          localStorage.setItem("token", response.data.token);
          axios.defaults.headers.common["Authorization"] =
            "Bearer " + response.data.token;
        }
        console.log(values.email)
        props.onLogin(values.email.toString());
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
          bg="gray.300"
        >
          <Box textAlign="center" mb={4}>
            <Heading size="md">Login to Deerhunt</Heading>
          </Box>
          <Box>
            <form onSubmit={handleSubmit(login)}>
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
              <Link
                onClick={() => {
                  window.location.href = "/signup";
                }}
              >
                <Box my={4}>
                  <Button width="full">Create An Account</Button>
                </Box>
              </Link>
            </form>
            <Box textAlign="center">
              <Link
                onClick={() => {
                  window.location.href = "/forgotpassword";
                }}
              >
                <Text>Forgot my password</Text>
              </Link>
            </Box>
          </Box>
        </Box>
      </Box>
    </Flex>
  );
}
