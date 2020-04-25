import React from "react";
import { Table } from "semantic-ui-react";

import { SerializableSubmissionListElem } from "../lib/find";

type Props = {
  submissions: SerializableSubmissionListElem[];
};

const SubmissionList: React.FC<Props> = (props) => {
  const submissionList = props.submissions.map((submission) => {
    let statusCell;

    // TODO: refresh for pending and grading request
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
        <Table.Cell>{submission.id}</Table.Cell>
        <Table.Cell>{submission.user.nickname}</Table.Cell>
        <Table.Cell>{submission.challenge.name}</Table.Cell>
        {statusCell}
        <Table.Cell>{submission.createdAt}</Table.Cell>
      </Table.Row>
    );
  });

  return (
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
  );
};

export default SubmissionList;
