import React from "react";
import { PrismaClient, ChallengeGetPayload } from "@prisma/client";
import { GetServerSideProps } from "next";
import { Container, Label, Header } from "semantic-ui-react";

import Layout from "../../components/Layout";

type Props = {
  challenge: ChallengeGetPayload<{
    include: {
      categories: true;
    };
  }>;
};

const prisma = new PrismaClient();

const Challenge: React.FC<Props> = (props) => {
  const chal = props.challenge;

  const categories = [];
  for (let category of chal.categories) {
    categories.push(
      <Label key={category.id} color="teal">
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
