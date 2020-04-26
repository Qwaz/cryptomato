import React from "react";
import { SubmissionGetPayload } from "@prisma/client";
import Error from "next/error";
import dynamic from "next/dynamic";
import JSONViewer from "react-json-viewer";
import { Container, Label, Header } from "semantic-ui-react";
import withSession, {
  GetServerSidePropsWithSession,
  getUserFromSession,
} from "../../lib/session";
import { normalizeId } from "../../lib/find";
import prisma from "../../lib/prisma";

import Layout from "../../components/Layout";

const CodeEditor = dynamic(import("../../components/CodeEditor"), {
  ssr: false,
});

type Props = {
  submission: SubmissionGetPayload<{
    select: {
      id: true;
      status: true;
      detail: true;
      code: true;
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
  }> | null;
};

const Submission: React.FC<Props> = (props) => {
  // TODO: automatic refresh
  const submission = props.submission;

  if (submission === null) {
    return <Error statusCode={404} />;
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
          <Header.Subheader>
            for {submission.challenge.name} by {submission.user.nickname}
          </Header.Subheader>
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

const getServerSidePropsWithSession: GetServerSidePropsWithSession<Props> = async ({
  req,
  params,
}) => {
  const NOT_FOUND = { props: { submission: null } };

  const submissionId = normalizeId(params.id);
  if (submissionId === null) {
    return NOT_FOUND;
  }

  let submission = await prisma.submission.findOne({
    where: {
      id: submissionId,
    },
    select: {
      id: true,
      status: true,
      detail: true,
      code: true,
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

  // do not show code if the user is not the author
  const user = getUserFromSession(req.session);
  if (!(user.isLoggedIn && user.id === submission.user.id)) {
    submission.code = "# This is not your submission";
  }

  return {
    props: {
      submission,
    },
  };
};

export const getServerSideProps = withSession(getServerSidePropsWithSession);

export default Submission;
