import { PrismaClient } from "@prisma/client";
import { NextApiRequest, NextApiResponse } from "next";

const prisma = new PrismaClient();

// POST /api/user
// Required fields in body: name, email
export default async function handle(
  req: NextApiRequest,
  res: NextApiResponse
) {
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

      return res.status(200).end();
    } catch (error) {
      errorArr.push(error.message);
    }
  }

  return res.status(400).json(errorArr);
}
