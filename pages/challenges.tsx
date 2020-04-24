import React from "react";
import { PrismaClient, Challenge } from "@prisma/client";
import { GetServerSideProps } from "next";
import { Container, List } from "semantic-ui-react";

import Layout from "../components/Layout";

type Props = {
  challenges: Challenge[];
};

const prisma = new PrismaClient();

const Challenges: React.FC<Props> = (props) => {
  return (
    <Layout>
      <Container>
        <List>
          {props.challenges.map((challenge) => {
            return <List.Item key={challenge.id}>{challenge.name}</List.Item>;
          })}
        </List>
      </Container>
    </Layout>
  );
};

export const getServerSideProps: GetServerSideProps = async () => {
  const pages = await prisma.challenge.findMany();

  return {
    props: { challenges: pages },
  };
};

export default Challenges;
