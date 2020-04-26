import React from "react";
import { ChallengeGetPayload } from "@prisma/client";
import { GetServerSideProps } from "next";
import Link from "next/link";
import { Container, Card, Rating, Label } from "semantic-ui-react";
import withSession, {
  User,
  getUserFromSession,
  GetServerSidePropsWithSession,
} from "../lib/session";
import prisma from "../lib/prisma";

import Layout from "../components/Layout";

type Props = {
  challenges: ChallengeGetPayload<{
    include: {
      categories: true;
      solvers: {
        select: {
          userId: true;
        };
      };
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
        <Card link color={challenge.solvers.length > 0 ? "green" : null}>
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

const getServerSidePropsWithSession: GetServerSidePropsWithSession<Props> = async ({
  req,
}) => {
  const user: User = getUserFromSession(req.session);
  const userId = user.isLoggedIn ? user.id : -1;

  const challenges = await prisma.challenge.findMany({
    include: {
      categories: true,
      solvers: {
        where: {
          userId: userId,
        },
        select: {
          userId: true,
        },
      },
    },
  });

  return {
    props: { challenges },
  };
};

export const getServerSideProps = withSession(getServerSidePropsWithSession);

export default Challenges;
