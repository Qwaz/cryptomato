import { exec } from "child_process";
import { SubmissionStatus } from "@prisma/client";
import { NextApiResponse } from "next";
import prisma from "../../../lib/prisma";
import withSession, { NextApiRequestWithSession } from "../../../lib/session";

export default withSession(
  async (req: NextApiRequestWithSession, res: NextApiResponse) => {
    const user = req.session.get("user");

    if (!user?.isLoggedIn) {
      // need login
      res.status(401).end();
      return;
    }

    const userId = user.id;

    const { challengeId, code } = await req.body;

    let submission = await prisma.submission.create({
      data: {
        code: code,
        status: SubmissionStatus.PENDING,
        user: {
          connect: {
            id: userId,
          },
        },
        challenge: {
          connect: {
            id: challengeId,
          },
        },
      },
    });

    exec(`node bin/grade.js ${submission.id}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`grading error: ${error.message}`);
        return;
      }
    });

    res.status(200).end();
  }
);
