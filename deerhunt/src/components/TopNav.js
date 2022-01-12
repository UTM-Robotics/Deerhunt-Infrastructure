import React from "react";
import { Box, Heading, Flex, Text, Button } from "@chakra-ui/react";
import { Link as RouteLink, useHistory } from "react-router-dom";

const MenuItems = ({ children }) => (
  <Text mt={{ base: 4, md: 0 }} mr={6} display="block">
    {children}
  </Text>
);

function TopNav(props) {
  const [show, setShow] = React.useState(false);
  const handleToggle = () => setShow(!show);
  const history = useHistory();
  const signOut = () => {
    localStorage.clear();
    window.history.replaceState({}, document.title);
    history.replace({ pathname: "/", state: {} });
    window.location.reload(true);
    history.push("/");
  };
  let loginButton;
  let signOutButton;
  if (localStorage.getItem("token")) {
    signOutButton = (
      <Button bg="transparent" border="1px" onClick={signOut}>
        Logout
      </Button>
    );
  } else {
    loginButton = (
      <RouteLink to="/login">
        <Button bg="transparent" border="1px">
          Login
        </Button>
      </RouteLink>
    );
  }
  return (
    <Flex
      as="nav"
      align="center"
      justify="space-between"
      wrap="wrap"
      padding="1.5rem"
      bg="#011627"
      color="white"
      {...props}
    >
      <Flex align="center" mr={5}>
        <RouteLink to="/">
          <Heading as="h1" size="md" letterSpacing={"-.1rem"}>
            Deerhunt Infrastructure
          </Heading>
        </RouteLink>
      </Flex>

      <Box display={{ base: "block", md: "none" }} onClick={handleToggle}>
        <svg
          fill="white"
          width="12px"
          viewBox="0 0 20 20"
          xmlns="http://www.w3.org/2000/svg"
        >
          <title>Menu</title>
          <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z" />
        </svg>
      </Box>

      <Box
        display={{ base: show ? "block" : "none", md: "flex" }}
        width={{ base: "full", md: "auto" }}
        alignItems="center"
        flexGrow={1}
      >
        <RouteLink to="/events">
          <MenuItems>Events</MenuItems>
        </RouteLink>
        {/*<RouteLink to={props.isloggedin ? "/myevents" : "/login"}>*/}
        {/*  <MenuItems>My Events</MenuItems>*/}
        {/*</RouteLink>*/}
        {/*<RouteLink to="/teams">*/}
        {/*  <MenuItems>Teams</MenuItems>*/}
        {/*</RouteLink>*/}
      </Box>
      <Box
        display={{ base: show ? "block" : "none", md: "block" }}
        mt={{ base: 4, md: 0 }}
      >
        {loginButton}
      </Box>
      <Box
        display={{ base: show ? "block" : "none", md: "block" }}
        mt={{ base: 4, md: 0 }}
      >
        {signOutButton}
      </Box>
    </Flex>
  );
}

export default TopNav;
