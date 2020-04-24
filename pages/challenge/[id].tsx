import React, { useState } from "react";
import { PrismaClient, ChallengeGetPayload } from "@prisma/client";
import { GetServerSideProps } from "next";
import dynamic from "next/dynamic";
import { Container, Label, Header } from "semantic-ui-react";

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

  return (
    <Layout>
      <Container>
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
        <LoginCheckButton />
      </Container>
    </Layout>
  );
};

export const getServerSideProps: GetServerSideProps = async (context) => {
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
