import React from "react";
import { Table } from "semantic-ui-react";

import { SerializableSubmission } from "../lib/find";
import Link from "next/link";
import useUser from "../lib/useUser";

type Props = {
  submissions: SerializableSubmission[];
};

const SubmissionList: React.FC<Props> = (props) => {
  // TODO: refresh for pending and grading request
  const { user } = useUser();

  const submissionList = props.submissions.map((submission) => {
    let submissionIdCell;
    if (user.isLoggedIn && user.id === submission.user.id) {
      submissionIdCell = (
        <Table.Cell>
          <Link href="/submissions/[id]" as={`/submissions/${submission.id}`}>
            <a>{submission.id}</a>
          </Link>
        </Table.Cell>
      );
    } else {
      submissionIdCell = <Table.Cell>{submission.id}</Table.Cell>;
    }

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
      case "UNKNOWN_ERROR": {
        statusCell = <Table.Cell negative>Unknown Error</Table.Cell>;
        break;
      }
    }
    return (
      <Table.Row key={submission.id}>
        {submissionIdCell}
        <Table.Cell>{submission.user.nickname}</Table.Cell>
        <Table.Cell>
          <Link
            href="/challenges/[id]"
            as={`/challenges/${submission.challenge.id}`}
          >
            <a>{submission.challenge.name}</a>
          </Link>
        </Table.Cell>
        {statusCell}
        <Table.Cell>{submission.createdAt}</Table.Cell>
      </Table.Row>
    );
  });

  return (
    <Table celled striped>
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
  );
};

export default SubmissionList;
