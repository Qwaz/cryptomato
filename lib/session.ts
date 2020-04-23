// this file is a wrapper with defaults to be used in both API routes and `getServerSideProps` functions
import withIronSession from "next-iron-session";
import { NextApiHandler, NextApiRequest } from "next";

export default function withSession(handler: NextApiHandler) {
  return withIronSession(handler, {
    password: process.env.SECRET_COOKIE_PASSWORD,
    cookieName: "cryptomato-session",
    cookieOptions: {
      // the next line allows to use the session in non-https environements like
      // Next.js dev mode (http://localhost:3000)
      secure: process.env.NODE_ENV === "production" ? true : false,
    },
  });
}

export type User =
  | {
      isLoggedIn: true;
      nickname: string;
      email: string;
    }
  | {
      isLoggedIn: false;
    };

export type Session = {
  user?: User;
  get: (key: "user") => User;
  set: (key: "user", value: User) => void;
  save: () => Promise<void>;
};

export type NextApiRequestWithSession = NextApiRequest & {
  session: Session;
};
