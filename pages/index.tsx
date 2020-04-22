import React from "react";
import { GetServerSideProps } from "next";
import Layout from "../components/Layout";
import fetch from "isomorphic-unfetch";
import Post, { PostProps } from "../components/Post";
import {
  Container,
  Header,
  Grid,
  Form,
  Button,
  Divider,
  Segment,
} from "semantic-ui-react";

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
        <Segment placeholder>
          <Grid columns={2} relaxed="very" stackable>
            <Grid.Column>
              <Form>
                <Form.Input
                  icon="user"
                  iconPosition="left"
                  label="Email"
                  placeholder="Email"
                />
                <Form.Input
                  icon="lock"
                  iconPosition="left"
                  label="Password"
                  placeholder="Password"
                  type="password"
                />

                <Button content="Login" primary />
              </Form>
            </Grid.Column>

            <Grid.Column verticalAlign="middle">
              <Button content="Sign up" icon="signup" size="big" positive />
            </Grid.Column>
          </Grid>

          <Divider vertical>Or</Divider>
        </Segment>
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
