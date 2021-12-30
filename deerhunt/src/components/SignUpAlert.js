import React from "react";
import { Alert, AlertIcon } from "@chakra-ui/react";
import { useStateValue } from "../statemanager/StateProvider";

function SignUpAlert(props) {
  const [{ userSignStatus, SignUpError }, dispatch] = useStateValue();
  // const textstatus1 = userSignStatus === "fail";
  // const textstatus2 = userSignStatus === "success";
  const error1 = props.error1;
  const setError = props.setError;

  const SuccessMessage = () => {
    return (
      <Alert status="success">
        <AlertIcon />
        Success! Check your email for a verification link.
      </Alert>
    );
  };

  const ErrorMessage = () => {
    return (
      <Alert status="error">
        <AlertIcon />

        {error1}
      </Alert>
    );
  };

  return (
    <div>
      {userSignStatus === "fail" ? ErrorMessage() : null}
      {userSignStatus === "success" ? SuccessMessage() : null}
    </div>
  );
}

export default SignUpAlert;
