import React from "react";
import { Container, Header } from "semantic-ui-react";

import Layout from "../components/Layout";
import Login from "../components/Login";

const Blog: React.FC = () => {
  return (
    <Layout>
      <Container>
        <Header as="h1">
          <Header.Content>
            Welcome to Cryptomato
            <Header.Subheader>
              A <i>fresh</i> approach to learn applied cryptography
            </Header.Subheader>
          </Header.Content>
        </Header>
        <Login />
      </Container>
    </Layout>
  );
};

export default Blog;
