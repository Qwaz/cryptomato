import React from "react";
import { PrismaClient, ChallengeGetPayload } from "@prisma/client";
import { GetServerSideProps } from "next";
import Router from "next/router";
import { Container, Card, Rating, Label } from "semantic-ui-react";

import Layout from "../components/Layout";

type Props = {
  challenges: ChallengeGetPayload<{
    include: {
      categories: true;
    };
  }>[];
};

const prisma = new PrismaClient();

const Challenges: React.FC<Props> = (props) => {
  const problemList = props.challenges.map((challenge) => {
    const categories = [];
    for (let category of challenge.categories) {
      categories.push(
        <Label key={category.id} color="teal">
          {category.name}
        </Label>
      );
    }
    return (
      <Card
        key={challenge.id}
        link
        onClick={() => Router.push(`/challenge/${challenge.id}`)}
      >
        <Card.Content>
          <Card.Header>{challenge.name}</Card.Header>
          <Card.Description>{challenge.description}</Card.Description>
        </Card.Content>
        <Card.Content extra>{categories}</Card.Content>
        <Card.Content extra>
          Difficulty:{" "}
          <Rating
            icon="star"
            defaultRating={challenge.level}
            maxRating={5}
            disabled
          />
        </Card.Content>
      </Card>
    );
  });
  return (
    <Layout>
      <Container>
        <Card.Group>{problemList}</Card.Group>
      </Container>
    </Layout>
  );
};

export const getServerSideProps: GetServerSideProps = async () => {
  const pages = await prisma.challenge.findMany({
    include: {
      categories: true,
    },
  });

  return {
    props: { challenges: pages },
  };
};

export default Challenges;
