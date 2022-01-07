import React from "react";
import ColourModeToggle from "./ColourModeToggle";
import TopNav from "./TopNav";

const LoginLayout = ({ children }) => {
  return (
    <div>
      <ColourModeToggle />
      {children}
    </div>
  );
};

const GeneralLayout = ({ children }) => {
  return (
    <div>
      <TopNav />
      <ColourModeToggle />
      {children}
    </div>
  );
};

export { LoginLayout, GeneralLayout };
