import { useEffect } from "react";
import Router from "next/router";
import useSWR from "swr";
import { User } from "./session";

export default function useUser(): {
  user: User;
  mutateUser: any;
} {
  let { data, mutate: mutateUser } = useSWR("/api/user");

  if (!data) {
    return {
      user: {
        isLoggedIn: false,
      },
      mutateUser,
    };
  } else {
    return {
      user: data,
      mutateUser,
    };
  }
}
