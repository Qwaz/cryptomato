import React from "react";
import { Button, ButtonProps, Label } from "semantic-ui-react";

import useUser from "../lib/useUser";
import Link from "next/link";

type Props = Omit<ButtonProps, "disabled">;

const LoginCheckButton: React.FC<Props> = (props) => {
  const { user } = useUser();
  const isLoggedIn = user?.isLoggedIn;

  return (
    <>
      <Button disabled={!isLoggedIn} primary {...props}>
        Submit
      </Button>
      {!isLoggedIn && (
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
