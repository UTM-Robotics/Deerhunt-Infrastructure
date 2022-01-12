import React from "react";
import { Text, HStack, IconButton, Link } from "@chakra-ui/react";
import { FaGithub, FaTwitter, FaInstagram, FaDiscord } from "react-icons/fa";

const ConnectWithUs = () => {
  return (
    <HStack>
      <Text pr={4}>Connect With Us</Text>
      <Link href="https://github.com/UTM-Robotics" isExternal>
        <IconButton isRound="true" icon={<FaGithub />}></IconButton>
      </Link>
      <Link href="https://twitter.com/utmrobotics" isExternal>
        <IconButton isRound="true" icon={<FaTwitter />} />
      </Link>
      <Link href="https://www.instagram.com/utm_robotics/" isExternal>
        <IconButton isRound="true" icon={<FaInstagram />} />
      </Link>
      <Link href="https://discord.gg/ueshFaMVq4" isExternal>
        <IconButton isRound="true" icon={<FaDiscord />} />
      </Link>
    </HStack>
  );
};

export default ConnectWithUs;
