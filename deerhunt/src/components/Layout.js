import React from "react";
import ColourModeToggle from "./ColourModeToggle";
import TopNav from "./TopNav";

const LoginLayout = ({ children }) => {
  return (
    <>
      <div>
        <ColourModeToggle />
      </div>
      <main>{children}</main>
    </>
  );
};

const GeneralLayout = ({ children }) => {
  return (
    <>
      <div>
        <TopNav />
        <ColourModeToggle />
      </div>
      <main>{children}</main>
    </>
  );
};

export { LoginLayout, GeneralLayout };
