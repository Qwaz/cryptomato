import React from "react";
import { SubmissionGetPayload } from "@prisma/client";
import { GetServerSideProps } from "next";
import Error from "next/error";
import dynamic from "next/dynamic";
import JSONViewer from "react-json-viewer";
import { Container, Label, Header } from "semantic-ui-react";
import prisma from "../../lib/prisma";
import useUser from "../../lib/useUser";
import { normalizeId, SerializableCreatedAt } from "../../lib/find";

import Layout from "../../components/Layout";

const CodeEditor = dynamic(import("../../components/CodeEditor"), {
  ssr: false,
});

type Props = {
  submission: SerializableCreatedAt<
    SubmissionGetPayload<{
      include: {
        challenge: {
          select: {
            id: true;
            name: true;
          };
        };
        user: {
          select: {
            id: true;
            nickname: true;
          };
        };
      };
    }>
  > | null;
};

const Submission: React.FC<Props> = (props) => {
  // TODO: refresh page
  const submission = props.submission;

  const { user } = useUser();

  if (submission === null) {
    return <Error statusCode={404} />;
  }

  if (!user.isLoggedIn) {
    return <Error statusCode={401} />;
  }

  if (user.id !== submission.user.id) {
    return <Error statusCode={403} />;
  }

  let statusLabel;
  switch (submission.status) {
    case "PENDING": {
      statusLabel = <Label size="large">Pending</Label>;
      break;
    }
    case "GRADING": {
      statusLabel = <Label size="large">Grading</Label>;
      break;
    }
    case "CORRECT": {
      statusLabel = (
        <Label size="large" color="green">
          Correct
        </Label>
      );
      break;
    }
    case "WRONG_ANSWER": {
      statusLabel = (
        <Label size="large" color="red">
          Wrong Answer
        </Label>
      );
      break;
    }
    case "RUNTIME_ERROR": {
      statusLabel = (
        <Label size="large" color="red">
          Runtime Error
        </Label>
      );
      break;
    }
    case "UNKNOWN_ERROR": {
      statusLabel = (
        <Label size="large" color="red">
          Unknown Error
        </Label>
      );
      break;
    }
  }

  let detailView = null;
  if (submission.detail !== null) {
    console.log(submission.detail);
    detailView = (
      <>
        <Header as="h2" dividing>
          Detail
        </Header>
        <JSONViewer json={JSON.parse(submission.detail)} />
      </>
    );
  }

  return (
    <Layout>
      <Container>
        <Header as="h1">
          Submission #{submission.id}
          {statusLabel}
          <Header.Subheader>for {submission.challenge.name}</Header.Subheader>
        </Header>

        {detailView}

        <Header as="h2" dividing>
          Code
        </Header>
        <CodeEditor value={submission.code} options={{ readOnly: true }} />
      </Container>
    </Layout>
  );
};

export const getServerSideProps: GetServerSideProps<Props> = async (
  context
) => {
  const NOT_FOUND = { props: { submission: null } };

  const submissionId = normalizeId(context.params.id);
  if (submissionId === null) {
    return NOT_FOUND;
  }

  // TODO: shouldn't leak submission detail to user
  const submission = await prisma.submission.findOne({
    where: {
      id: submissionId,
    },
    include: {
      challenge: {
        select: {
          id: true,
          name: true,
        },
      },
      user: {
        select: {
          id: true,
          nickname: true,
        },
      },
    },
  });

  if (submission === null) {
    return NOT_FOUND;
  }

  const serializableSubmission = {
    ...submission,
    createdAt: submission.createdAt.toLocaleString(),
  };

  return {
    props: {
      submission: serializableSubmission,
    },
  };
};

export default Submission;
