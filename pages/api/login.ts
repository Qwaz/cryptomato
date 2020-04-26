import { NextApiResponse } from "next";
import bcrypt from "bcrypt";
import prisma from "../../lib/prisma";
import withSession, { NextApiRequestWithSession } from "../../lib/session";

export default withSession(
  async (req: NextApiRequestWithSession, res: NextApiResponse) => {
    const { email, password } = await req.body;

    const user = await prisma.user.findOne({
      where: {
        email: email,
      },
    });

    if (user && bcrypt.compareSync(password, user.password)) {
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
