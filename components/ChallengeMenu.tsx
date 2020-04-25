import React from "react";
import { Menu } from "semantic-ui-react";
import Link from "next/link";

type Props = {
  id: number;
  active: "problem" | "solvers" | "submissions";
};

const ChallengeMenu: React.FC<Props> = (props) => {
  return (
    <Menu pointing secondary>
      <Link href="/challenges/[id]" as={`/challenges/${props.id}`}>
        <Menu.Item name="problem" active={props.active === "problem"} />
      </Link>
      <Link
        href="/challenges/[id]/solvers"
        as={`/challenges/${props.id}/solvers`}
      >
        <Menu.Item name="solvers" active={props.active === "solvers"} />
      </Link>
      <Link
        href="/challenges/[id]/submissions"
        as={`/challenges/${props.id}/submissions`}
      >
        <Menu.Item name="submissions" active={props.active === "submissions"} />
      </Link>
    </Menu>
  );
};

export default ChallengeMenu;
