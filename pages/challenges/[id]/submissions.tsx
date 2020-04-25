import React from "react";
import { Challenge } from "@prisma/client";
import { GetServerSideProps } from "next";
import Error from "next/error";
import { Container } from "semantic-ui-react";

import Layout from "../../../components/Layout";
import ChallengeMenu from "../../../components/ChallengeMenu";
import {
  findChallengeWithStringId,
  SerializableSubmissionListElem,
  findSerializableSubmissions,
} from "../../../lib/find";
import SubmissionList from "../../../components/SubmissionList";

type Props = {
  challenge: Challenge | null;
  submissions: SerializableSubmissionListElem[];
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
  const challenge = await findChallengeWithStringId(context.params.id);
  if (challenge === null) {
    return { props: { challenge: null, submissions: [] } };
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
