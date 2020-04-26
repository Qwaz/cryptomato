import React, { useState } from "react";
import { ChallengeGetPayload } from "@prisma/client";
import { GetServerSideProps } from "next";
import Error from "next/error";
import Router from "next/router";
import dynamic from "next/dynamic";
import { Container, Label, Header, Segment } from "semantic-ui-react";
import prisma from "../../lib/prisma";
import { normalizeId } from "../../lib/find";

import Layout from "../../components/Layout";
import LoginCheckButton from "../../components/LoginCheckButton";
import ChallengeMenu from "../../components/ChallengeMenu";

const CodeEditor = dynamic(import("../../components/CodeEditor"), {
  ssr: false,
});

type Props = {
  challenge: ChallengeGetPayload<{
    include: {
      categories: true;
    };
  }> | null;
};

const Challenge: React.FC<Props> = (props) => {
  const [loading, setLoading] = useState(false);

  const [code, setCode] = useState("");

  if (props.challenge === null) {
    return <Error statusCode={404} />;
  }

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
        const submissionId = (await res.json()).id;
        Router.push(`/submissions/${submissionId}`);
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
        <ChallengeMenu id={chal.id} active="problem" />

        <Segment loading={loading}>
          <Header as="h1" dividing>
            {chal.name}
            {categories}
          </Header>
          <p>{chal.description}</p>

          <Header as="h2" dividing>
            Code
          </Header>
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
  const challengeId = normalizeId(context.params.id);
  if (challengeId === null) {
    return { props: null };
  }

  return {
    props: {
      challenge: await prisma.challenge.findOne({
        where: { id: challengeId },
        include: { categories: true },
      }),
    },
  };
};

export default Challenge;
