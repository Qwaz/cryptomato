import React from "react";
import { GetServerSideProps } from "next";
import { Container } from "semantic-ui-react";

import Layout from "../components/Layout";
import SubmissionList from "../components/SubmissionList";
import {
  findSerializableSubmissions,
  SerializableSubmission,
} from "../lib/find";

type Props = {
  submissions: SerializableSubmission[];
};

const Submissions: React.FC<Props> = (props) => {
  return (
    <Layout>
      <Container>
        <SubmissionList submissions={props.submissions} />
      </Container>
    </Layout>
  );
};

export const getServerSideProps: GetServerSideProps<Props> = async () => {
  // TODO: pagination
  return {
    props: {
      submissions: await findSerializableSubmissions({
        orderBy: {
          createdAt: "desc",
        },
      }),
    },
  };
};

export default Submissions;
