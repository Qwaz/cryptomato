// this file is a wrapper with defaults to be used in both API routes and `getServerSideProps` functions
import withIronSession from "next-iron-session";
import { NextApiRequest, NextApiResponse } from "next";
import { ParsedUrlQuery } from "querystring";
import { IncomingMessage, ServerResponse } from "http";

export type User =
  | {
      isLoggedIn: true;
      id: number;
      nickname: string;
      email: string;
    }
  | {
      isLoggedIn: false;
    };

export type Session = {
  get: (key: "user") => User | null;
  set: (key: "user", value: User) => void;
  save: () => Promise<void>;
  destroy: () => void;
};

export type NextApiRequestWithSession = NextApiRequest & {
  session: Session;
};

export type NextApiHandlerWithSession<T = any> = (
  req: NextApiRequestWithSession,
  res: NextApiResponse<T>
) => void;

export type GetServerSidePropsWithSession<
  P extends { [key: string]: any } = { [key: string]: any },
  Q extends ParsedUrlQuery = ParsedUrlQuery
> = (context: {
  req: IncomingMessage & { session: Session };
  res: ServerResponse;
  params?: Q;
  query: ParsedUrlQuery;
  preview?: boolean;
  previewData?: any;
}) => Promise<{ props: P }>;

export default function withSession(
  handler: NextApiHandlerWithSession | GetServerSidePropsWithSession
) {
  return withIronSession(handler, {
    password: process.env.SECRET_COOKIE_PASSWORD,
    cookieName: "cryptomato-session",
    cookieOptions: {
      // the next line allows to use the session in non-https environments like
      // Next.js dev mode (http://localhost:3000)
      secure: process.env.NODE_ENV === "production" ? true : false,
    },
  });
}

export function getUserFromSession(session: Session): User {
  const user = session.get("user");
  if (user?.isLoggedIn) {
    return user;
  } else {
    return {
      isLoggedIn: false,
    };
  }
}
