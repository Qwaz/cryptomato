import React from "react";
import {
  PrismaClient,
  SubmissionGetPayload,
  SubmissionStatus,
} from "@prisma/client";
import { GetServerSideProps } from "next";
import { Table, Container } from "semantic-ui-react";

import Layout from "../components/Layout";

type Props = {
  submissions: (SubmissionGetPayload<{
    select: {
      id: true;
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
      status: true;
    };
  }> & { createdAt: string })[];
};

const prisma = new PrismaClient();

const Submissions: React.FC<Props> = (props) => {
  const submissionList = props.submissions.map((submission) => {
    let statusCell;

    switch (submission.status) {
      case "PENDING": {
        statusCell = <Table.Cell>Pending</Table.Cell>;
        break;
      }
      case "GRADING": {
        statusCell = <Table.Cell>Grading</Table.Cell>;
        break;
      }
      case "CORRECT": {
        statusCell = <Table.Cell positive>Correct</Table.Cell>;
        break;
      }
      case "WRONG_ANSWER": {
        statusCell = <Table.Cell negative>Wrong Answer</Table.Cell>;
        break;
      }
      case "RUNTIME_ERROR": {
        statusCell = <Table.Cell negative>Runtime Error</Table.Cell>;
        break;
      }
    }
    return (
      <Table.Row key={submission.id}>
        <Table.Cell>{submission.id}</Table.Cell>
        <Table.Cell>{submission.user.nickname}</Table.Cell>
        <Table.Cell>{submission.challenge.name}</Table.Cell>
        {statusCell}
        <Table.Cell>{submission.createdAt}</Table.Cell>
      </Table.Row>
    );
  });
  return (
    <Layout>
      <Container>
        <Table celled>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell>ID</Table.HeaderCell>
              <Table.HeaderCell>User</Table.HeaderCell>
              <Table.HeaderCell>Challenge</Table.HeaderCell>
              <Table.HeaderCell>Status</Table.HeaderCell>
              <Table.HeaderCell>Submission Time</Table.HeaderCell>
            </Table.Row>
          </Table.Header>

          <Table.Body>{submissionList}</Table.Body>
        </Table>
      </Container>
    </Layout>
  );
};

export const getServerSideProps: GetServerSideProps<Props> = async () => {
  // TODO: pagination
  const submissions = await prisma.submission.findMany({
    select: {
      id: true,
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
      createdAt: true,
      status: true,
    },
    orderBy: {
      createdAt: "desc",
    },
  });

  const serializableSubmissions = submissions.map((submission) => {
    return {
      ...submission,
      createdAt: submission.createdAt.toLocaleString(),
    };
  });

  return {
    props: { submissions: serializableSubmissions },
  };
};

export default Submissions;
