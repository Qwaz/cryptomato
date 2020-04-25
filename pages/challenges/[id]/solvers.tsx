import React from "react";
import { SolveLogGetPayload } from "@prisma/client";
import { GetServerSideProps } from "next";
import Error from "next/error";
import { Container, Table } from "semantic-ui-react";

import Layout from "../../../components/Layout";
import { findChallengeWithStringId } from "../../../lib/find";
import ChallengeMenu from "../../../components/ChallengeMenu";

type Props = {
  challengeId: number | null;
  solveLog: (Omit<
    SolveLogGetPayload<{
      include: {
        user: true;
      };
    }>,
    "createdAt"
  > & { createdAt: string })[];
};

const Solvers: React.FC<Props> = (props) => {
  if (props.challengeId === null) {
    return <Error statusCode={404} />;
  }

  for (const solver of props.solveLog) {
    console.log(solver);
  }

  return (
    <Layout>
      <Container>
        <ChallengeMenu id={props.challengeId} active="solvers" />
        {props.solveLog.length == 0 ? (
          <p>No one has solved this problem yet. Be the first!</p>
        ) : (
          <Table celled>
            <Table.Header>
              <Table.Row>
                <Table.HeaderCell>Rank</Table.HeaderCell>
                <Table.HeaderCell>User</Table.HeaderCell>
                <Table.HeaderCell>Solve Time</Table.HeaderCell>
              </Table.Row>
            </Table.Header>

            <Table.Body>
              {props.solveLog.map((solveLog, i) => (
                <Table.Row key={solveLog.submissionId}>
                  <Table.Cell>{i + 1}</Table.Cell>
                  <Table.Cell>{solveLog.user.nickname}</Table.Cell>
                  <Table.Cell>{solveLog.createdAt}</Table.Cell>
                </Table.Row>
              ))}
            </Table.Body>
          </Table>
        )}
      </Container>
    </Layout>
  );
};

export const getServerSideProps: GetServerSideProps<Props> = async (
  context
) => {
  const challenge = await findChallengeWithStringId(context.params.id, {
    solvers: {
      orderBy: {
        createdAt: "asc",
      },
      include: {
        user: true,
      },
    },
  });

  // TODO: pagination
  if (challenge) {
    return {
      props: {
        challengeId: challenge.id,
        solveLog: challenge.solvers.map((solveLog) => ({
          ...solveLog,
          createdAt: solveLog.createdAt.toLocaleString(),
        })),
      },
    };
  }

  return { props: { challengeId: null, solveLog: [] } };
};

export default Solvers;
