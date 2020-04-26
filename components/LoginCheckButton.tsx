import React from "react";
import { Button, ButtonProps, Label } from "semantic-ui-react";

import useUser from "../lib/useUser";
import Link from "next/link";

type Props = Omit<ButtonProps, "disabled">;

const LoginCheckButton: React.FC<Props> = (props) => {
  const { user } = useUser();

  return (
    <>
      <Button disabled={!user.isLoggedIn} primary {...props}>
        Submit
      </Button>
      {!user.isLoggedIn && (
        <Link href="/">
          <Label as="a" basic color="red" pointing="left">
            Please Login to Submit
          </Label>
        </Link>
      )}
    </>
  );
};

export default LoginCheckButton;
