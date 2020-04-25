import { PrismaClient } from "@prisma/client";
import { NextApiResponse } from "next";
import withSession, { NextApiRequestWithSession } from "../../lib/session";

const prisma = new PrismaClient();

export default withSession(
  async (req: NextApiRequestWithSession, res: NextApiResponse) => {
    const { email, password } = await req.body;

    // TODO: hash password
    const userArr = await prisma.user.findMany({
      where: {
        email: email,
        password: password,
      },
      first: 1,
    });
    const user = userArr[0];

    if (user) {
      req.session.set("user", {
        isLoggedIn: true,
        id: user.id,
        nickname: user.nickname,
        email: user.email,
      });
      await req.session.save();
      res.json(user);
    } else {
      res
        .status(401)
        .json(["Login failed; Please check your email and password"]);
    }
  }
);
