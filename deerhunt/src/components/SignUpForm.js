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
 
} from "@chakra-ui/react";
import { useHistory } from "react-router-dom";
import { useStateValue } from "../statemanager/StateProvider";
import axios from "axios";



export default function SignUpForm(props) {
  const [{ userSignStatus}, dispatch] =useStateValue();
  const error1 = props.error1;
  const setError = props.setError;
  const {
    handleSubmit,
    register,
    formState: { isSubmitting },
  } = useForm();
  const history = useHistory();
  async function SignUp(values) {
    console.log(values);
    var form = new FormData();
    form.append("email", values.email);
    form.append("password", values.password);
    await axios
      .post("http://127.0.0.1:5000/api/user", form)
      .then((response) => {
        dispatch({
          type: "SIGNED_UP",
        });
        history.push("/login");
      })
      .catch((error) => {
      
        setError(error.response.data.message);

        dispatch({
          type: "SignUpFail",
          
        });
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
                      message: "Minimum length should be 4",
                    },
                  })}
                />
              </FormControl>
              <Box my={4}>
                <Button width="full" isLoading={isSubmitting} type="submit">
                  Sign Up
                </Button>
              </Box>
              <Link
                onClick={() => {
                  window.location.href = "/login";
                }}
              >
                <Box my={4}>
                  <Button width="full">I already have an account</Button>
                </Box>
              </Link>
            </form>
          </Box>
        </Box>
      </Box>
    </Flex>
  );
}

