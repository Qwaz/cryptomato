import React from "react";
import { Challenge } from "@prisma/client";
import { GetServerSideProps } from "next";
import Error from "next/error";
import { Container } from "semantic-ui-react";
import prisma from "../../../lib/prisma";

import Layout from "../../../components/Layout";
import ChallengeMenu from "../../../components/ChallengeMenu";
import SubmissionList from "../../../components/SubmissionList";
import {
  SerializableSubmission,
  findSerializableSubmissions,
  normalizeId,
} from "../../../lib/find";

type Props = {
  challenge: Challenge | null;
  submissions: SerializableSubmission[];
};

const Submissions: React.FC<Props> = (props) => {
  if (props.challenge === null) {
    return <Error statusCode={404} />;
  }

  return (
    <Layout>
      <Container>
        <ChallengeMenu id={props.challenge.id} active="submissions" />
        <SubmissionList submissions={props.submissions} />
      </Container>
    </Layout>
  );
};

export const getServerSideProps: GetServerSideProps<Props> = async (
  context
) => {
  const NOT_FOUND = { props: { challenge: null, submissions: [] } };

  const challengeId = normalizeId(context.params.id);
  if (challengeId === null) {
    return NOT_FOUND;
  }

  const challenge = await prisma.challenge.findOne({
    where: { id: challengeId },
  });
  if (challenge === null) {
    return NOT_FOUND;
  }

  // TODO: pagination
  return {
    props: {
      challenge,
      submissions: await findSerializableSubmissions({
        where: {
          challengeId: challenge.id,
        },
        orderBy: {
          createdAt: "desc",
        },
      }),
    },
  };
};

export default Submissions;
