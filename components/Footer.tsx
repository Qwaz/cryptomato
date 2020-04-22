import React from "react";
import { useRouter } from "next/router";
import { Segment, Container, Divider } from "semantic-ui-react";

const Footer: React.FC = () => {
  const router = useRouter();

  return (
    <Container
      textAlign="center"
      style={{ margin: "5em 0em 0em", padding: "5em 0em" }}
    >
      <Divider />
      <p>{"\u00A9"} 2020 Cryptomato Project</p>
      <p>CS 6260 Spring 2020</p>
    </Container>
  );
};

export default Footer;
