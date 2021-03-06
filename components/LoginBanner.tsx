import React, { useState } from "react";
import isoFetch from "isomorphic-unfetch";
import Router from "next/router";
import {
  Segment,
  Grid,
  Form,
  Button,
  Divider,
  Message,
  Header,
} from "semantic-ui-react";
import useUser from "../lib/useUser";
import Link from "next/link";

const LoginBanner: React.FC = () => {
  const { user, mutateUser } = useUser();

  const [loading, setLoading] = useState(false);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [error, setError] = useState([]);

  const submitData = async (e: React.SyntheticEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const body = { email, password };

      const res = await isoFetch(`/api/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (res.ok) {
        mutateUser();
        setError([]);
      } else {
        setError(await res.json());
      }
    } catch (error) {
      console.error(error);
      alert(error);
    }
    setLoading(false);
  };

  return (
    <>
      <Segment placeholder>
        {user.isLoggedIn ? (
          <>
            <Header as="h2" textAlign="center">
              Welcome, {user.nickname}!
            </Header>
            <Link href="/challenges">
              <Button
                content="Let's go!"
                icon="right arrow"
                labelPosition="right"
                color="red"
              />
            </Link>
          </>
        ) : (
          <>
            <Grid columns={2} relaxed="very" stackable>
              <Grid.Column>
                <Form loading={loading} onSubmit={submitData}>
                  <Form.Input
                    icon="user"
                    iconPosition="left"
                    label="Email"
                    placeholder="Email"
                    type="text"
                    onChange={(e) => setEmail(e.target.value)}
                  />
                  <Form.Input
                    icon="lock"
                    iconPosition="left"
                    label="Password"
                    placeholder="Password"
                    type="password"
                    onChange={(e) => setPassword(e.target.value)}
                  />

                  <Button content="Login" />
                </Form>
              </Grid.Column>

              <Grid.Column verticalAlign="middle">
                <Button
                  content="Sign Up"
                  icon="signup"
                  size="big"
                  primary
                  onClick={() => Router.push("/signup")}
                />
              </Grid.Column>
            </Grid>

            <Divider vertical>Or</Divider>
          </>
        )}
      </Segment>
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
    </>
  );
};

export default LoginBanner;
