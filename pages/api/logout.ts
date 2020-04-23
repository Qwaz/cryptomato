import { mutate } from "swr";
import { NextApiResponse } from "next";
import withSession, { NextApiRequestWithSession } from "../../lib/session";

export default withSession(
  async (req: NextApiRequestWithSession, res: NextApiResponse) => {
    req.session.destroy();
    mutate("/api/user");
    res.end();
  }
);
