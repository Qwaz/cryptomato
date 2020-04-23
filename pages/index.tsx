import React from "react";
import fetch from "isomorphic-unfetch";
import { GetServerSideProps } from "next";
import { Container, Header } from "semantic-ui-react";

import Layout from "../components/Layout";
import { PostProps } from "../components/Post";
import Login from "../components/Login";

type Props = {
  feed: PostProps[];
};

const Blog: React.FC<Props> = (props) => {
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

export const getServerSideProps: GetServerSideProps = async () => {
  const res = await fetch("http://localhost:3000/api/feed");
  const feed = await res.json();
  return {
    props: { feed },
  };
};

export default Blog;
