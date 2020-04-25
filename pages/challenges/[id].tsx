import React, { useState } from "react";
import { PrismaClient, ChallengeGetPayload } from "@prisma/client";
import { GetServerSideProps } from "next";
import Router from "next/router";
import dynamic from "next/dynamic";
import { Container, Label, Header, Segment } from "semantic-ui-react";

import Layout from "../../components/Layout";
import LoginCheckButton from "../../components/LoginCheckButton";

const CodeEditor = dynamic(import("../../components/CodeEditor"), {
  ssr: false,
});

type Props = {
  challenge: ChallengeGetPayload<{
    include: {
      categories: true;
    };
  }>;
};

const prisma = new PrismaClient();

const Challenge: React.FC<Props> = (props) => {
  const [loading, setLoading] = useState(false);

  const [code, setCode] = useState("");

  const chal = props.challenge;

  const categories = [];
  for (let category of chal.categories) {
    categories.push(
      <Label key={category.id} color="red" size="small">
        {category.name}
      </Label>
    );
  }

  const submitData = async (e: React.SyntheticEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const body = { challengeId: chal.id, code };

      const res = await fetch(`/api/challenge/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (res.ok) {
        Router.push("/challenges");
      } else {
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
      <Container>
        <Segment loading={loading}>
          <Header as="h1" dividing>
            {chal.name}
            {categories}
          </Header>
          <p>{chal.description}</p>

          <Header as="h2">Code</Header>
          <CodeEditor
            value={code}
            onBeforeChange={(editor, data, value) => {
              setCode(value);
            }}
          />

          <LoginCheckButton onClick={submitData} />
        </Segment>
      </Container>
    </Layout>
  );
};

export const getServerSideProps: GetServerSideProps<Props> = async (
  context
) => {
  const challengeIdString = context.params.id as string;
  if (challengeIdString.match(/^[1-9]\d*$/)) {
    const challengeIdNumber = parseInt(challengeIdString);
    const challenge = await prisma.challenge.findOne({
      where: {
        id: challengeIdNumber,
      },
      include: {
        categories: true,
      },
    });
    if (challenge) {
      return { props: { challenge } };
    }
  }
  throw new Error("Invalid path");
};

export default Challenge;
