import { NextApiRequest, NextApiResponse } from "next";
import bcrypt from "bcrypt";
import prisma from "../../lib/prisma";
import withSession, {
  NextApiRequestWithSession,
  getUserFromSession,
} from "../../lib/session";

export default async function handle(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === "GET") {
    await withSession(handleGET)(req, res);
  } else if (req.method === "POST") {
    await withSession(handlePOST)(req, res);
  } else {
    res.status(405).end();
  }
}

// GET /api/user
// Always return valid User type
async function handleGET(req: NextApiRequestWithSession, res: NextApiResponse) {
  // TODO: check whether the user still exists
  const user = getUserFromSession(req.session);
  res.json(user);
}

// POST /api/user
// Required fields in body: nickname, email, password
async function handlePOST(
  req: NextApiRequestWithSession,
  res: NextApiResponse
) {
  const { nickname, email, password } = req.body;

  let errorArr = [];
  if (nickname.length < 4 || nickname.length > 20) {
    errorArr.push("Nickname length should be between 4 to 20");
  }

  const emailPattern = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
  if (!emailPattern.test(email)) {
    errorArr.push("Invalid email address");
  }

  if (password.length < 8) {
    errorArr.push("Password length should be at least 8 characters long");
  }

  if (errorArr.length == 0) {
    if (
      (await prisma.user.findOne({
        where: {
          nickname: nickname,
        },
      })) !== null
    ) {
      errorArr.push("Nickname has been already taken");
    }

    if (
      (await prisma.user.findOne({
        where: {
          email: email,
        },
      })) !== null
    ) {
      errorArr.push("Already registered email");
    }
  }

  if (errorArr.length == 0) {
    try {
      const passwordHash = bcrypt.hashSync(password, bcrypt.genSaltSync(10));
      const user = await prisma.user.create({
        data: {
          email: email,
          nickname: nickname,
          password: passwordHash,
        },
      });

      // login a user
      req.session.set("user", {
        isLoggedIn: true,
        id: user.id,
        nickname: user.nickname,
        email: user.email,
      });
      await req.session.save();

      res.status(200).end();
      return;
    } catch (error) {
      errorArr.push(error.message);
    }
  }

  res.status(400).json(errorArr);
}
