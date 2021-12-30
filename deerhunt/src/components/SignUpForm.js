import React from "react";
import { useForm } from "react-hook-form";
import {
  Flex,
  Box,
  Heading,
  FormControl,
  FormLabel,
  FormHelperText,
  Input,
  Button,
  Link,
  Text,
} from "@chakra-ui/react";
import { useHistory } from "react-router-dom";
import { useStateValue } from "../statemanager/StateProvider";
import axios from "../config/config";



export default function SignUpForm(props) {
  // eslint-disable-next-line 
  const [{ input, setInput}, dispatch] = useStateValue();
  
  const setError = props.setError;
  const {
    handleSubmit,
    register,
    formState: {errors, isSubmitting },
  } = useForm();
  const history = useHistory();
  async function SignUp(values) {
    var form = new FormData();
    console.log(axios.defaults.baseURL);
    form.append("email", values.email);
    form.append("password", values.password);
    await axios
      .post("api/user", form)
      .then((response) => {
        dispatch({
          type: "SIGNED_UP",
        });
        history.push("/login");
      })
      .catch((error) => {
        if (error.response) {
          setError(error.response.data.message);
          dispatch({
            type: "SignUpFail",
          });
        }
        else if (error.request) {
          setError("Something went wrong! The request failed.");
          dispatch({
            type: "SignUpFail",
          });
        }
        else {
          setError("Something went wrong! Could not make request.");
          dispatch({
            type: "SignUpFail",
          });
        }
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
            <Heading size="md">Signup for Deerhunt</Heading>
          </Box>
          <Box>
            <form onSubmit={handleSubmit(SignUp)}>
              <FormControl isInvalid={errors.email}>
                <FormLabel>Email</FormLabel>
                <Input

                  id='email'
                  type="email"
                  placeholder="Enter your UofT email"
                  {...register("email", {
                    required: "This is required",
                  })}
                />
            <FormHelperText>Use either @mail.utoronto.ca or @utoronto.ca </FormHelperText>
              </FormControl>
              <FormControl mt={4} isInvalid={errors.password}>
                <FormLabel>Password</FormLabel>
                <Input
                  id='password'
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
                <FormHelperText>Minimum password length of 8.</FormHelperText>
              </FormControl>
              <Box my={4}>
                <Button width="full" isLoading={isSubmitting} type="submit">
                  Sign Up
                </Button>
              </Box>
              <Box textAlign="center">
                <Link
                  onClick={() => {
                    window.location.href = "/login";
                  }}
                >
                  <Text>I already have an account</Text>
                </Link>
              </Box>
            </form>
          </Box>
        </Box>
      </Box>
    </Flex>
  );
}

