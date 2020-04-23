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
  Message,
} from "semantic-ui-react";

const SignUp: React.FC = () => {
  const [loading, setLoading] = useState(false);

  const [nickname, setNickname] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState([]);

  const submitData = async (e: React.SyntheticEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const body = { nickname, email, password };

      const res = await fetch(`http://localhost:3000/api/user`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (res.ok) {
        Router.push("/");
      } else {
        setError(await res.json());
        setLoading(false);
      }
    } catch (error) {
      console.error(error);
      alert(error);
      setLoading(false);
    }
  };

  return (
    <Layout>
      <Container text>
        <Form loading={loading} onSubmit={submitData}>
          <Header as="h1">Sign Up</Header>
          <Form.Input
            label="Nickname"
            icon="user"
            iconPosition="left"
            placeholder="George Burdell"
            type="text"
            onChange={(e) => setNickname(e.target.value)}
          />
          <Form.Input
            label="Email"
            icon="mail"
            iconPosition="left"
            placeholder="george.burdell@gathech.edu"
            type="text"
            onChange={(e) => setEmail(e.target.value)}
          />
          <Form.Input
            label="Password"
            icon="lock"
            iconPosition="left"
            placeholder="minimum 8 characters"
            type="password"
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button type="submit">Submit</Button>
        </Form>
        {error.length > 0 && (
          <Message negative>
            <Message.Header>
              There was an error processing your request
            </Message.Header>
            <ul>
              {error.map((value, index) => {
                return <li key={index}>{value}</li>;
              })}
            </ul>
          </Message>
        )}
      </Container>
    </Layout>
  );
};

export default SignUp;
