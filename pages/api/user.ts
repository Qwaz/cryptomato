import { PrismaClient } from "@prisma/client";
import { NextApiRequest, NextApiResponse } from "next";
import withSession, { NextApiRequestWithSession } from "../../lib/session";

const prisma = new PrismaClient();

export default async function handle(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === "GET") {
    await withSession(handleGET)(req, res);
  } else if (req.method === "POST") {
    await handlePOST(req, res);
  } else {
    res.status(405).end();
  }
}

// GET /api/user
async function handleGET(req: NextApiRequestWithSession, res: NextApiResponse) {
  const user = req.session.get("user");
  if (user?.isLoggedIn) {
    res.json(user);
  } else {
    res.json({
      isLoggedIn: false,
    });
  }
}

// POST /api/user
// Required fields in body: nickname, email, password
async function handlePOST(req: NextApiRequest, res: NextApiResponse) {
  // TODO: hash password
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
    errorArr.push("Password leght should be at least 8 characters long");
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
      const result = await prisma.user.create({
        data: {
          email: email,
          nickname: nickname,
          password: password,
        },
      });

      // TODO: login a user
      console.log(result);

      res.status(200).end();
      return;
    } catch (error) {
      errorArr.push(error.message);
    }
  }

  res.status(400).json(errorArr);
}
