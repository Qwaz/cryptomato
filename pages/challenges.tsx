import React from "react";
import { ChallengeGetPayload } from "@prisma/client";
import { GetServerSideProps } from "next";
import Link from "next/link";
import { Container, Card, Rating, Label } from "semantic-ui-react";
import prisma from "../lib/prisma";

import Layout from "../components/Layout";

type Props = {
  challenges: ChallengeGetPayload<{
    include: {
      categories: true;
    };
  }>[];
};

const Challenges: React.FC<Props> = (props) => {
  const problemList = props.challenges.map((challenge) => {
    const categories = [];
    for (let category of challenge.categories) {
      categories.push(
        <Label key={category.id} color="red">
          {category.name}
        </Label>
      );
    }
    return (
      <Link
        href="/challenges/[id]"
        as={`/challenges/${challenge.id}`}
        key={challenge.id}
      >
        <Card link>
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
      </Link>
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

export const getServerSideProps: GetServerSideProps<Props> = async () => {
  const challenges = await prisma.challenge.findMany({
    include: {
      categories: true,
    },
  });

  return {
    props: { challenges },
  };
};

export default Challenges;
