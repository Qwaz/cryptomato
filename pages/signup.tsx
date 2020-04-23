import React, { useState } from "react";
import fetch from "isomorphic-unfetch";
import Router from "next/router";
import Layout from "../components/Layout";
import {
  Form,
  Header,
  Container,
  Input,
  Icon,
  Button,
} from "semantic-ui-react";

const SignUp: React.FC = () => {
  const [loading, setLoading] = useState(false);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const submitData = async (e: React.SyntheticEvent) => {
    e.preventDefault();
    try {
      const body = { name, email };
      const res = await fetch(`http://localhost:3000/api/user`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      const data = await res.json();
      Router.push("/");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Layout>
      <Container text>
        <Form loading={loading}>
          <Header as="h1">Sign Up</Header>
          <Form.Field>
            <label>Nickname</label>
            <Input
              icon="user"
              iconPosition="left"
              placeholder="George Burdell"
              type="text"
            />
          </Form.Field>
          <Form.Field>
            <label>Email</label>
            <Input
              icon="mail"
              iconPosition="left"
              placeholder="george.burdell@gathech.edu"
              type="text"
            />
          </Form.Field>
          <Form.Field>
            <label>Password</label>
            <Input
              icon="lock"
              iconPosition="left"
              placeholder="minimum 8 characters"
              type="password"
            />
          </Form.Field>
          <Button type="submit">Submit</Button>
        </Form>
      </Container>
    </Layout>
  );
};

export default SignUp;
