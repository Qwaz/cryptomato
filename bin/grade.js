const { PrismaClient, SubmissionStatus } = require("@prisma/client");

const prisma = new PrismaClient();
const submissionId = parseInt(process.argv[2]);

function choose(choices) {
  var index = Math.floor(Math.random() * choices.length);
  return choices[index];
}

const upsertSolveLog = async (userId, challengeId, submissionId) => {
  await prisma.solveLog.upsert({
    create: {
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
      submission: {
        connect: {
          id: submissionId,
        },
      },
    },
    update: {},
    where: {
      userId_challengeId: {
        userId: userId,
        challengeId: challengeId,
      },
    },
  });
};

async function main() {
  // first, set the state to grading
  const { code } = await prisma.submission.update({
    data: {
      status: SubmissionStatus.GRADING,
    },
    where: {
      id: submissionId,
    },
    select: {
      code: true,
    },
  });

  /*
  type RpcResult =
    | {
        type: "success",
        solved: boolean,
        detail: any,
        user_code_output: string,
      }
    | {
        type: "Exception",
        message: string,
      }
    | {
        type: "CalledProcessError",
        message: string,
      };
  */

  // TODO: invoke gRPC worker and get the result
  const result = choose([
    {
      type: "success",
      solved: true,
      detail: {},
      user_code_output: "Is this success?",
    },
    {
      type: "success",
      solved: false,
      detail: {},
      user_code_output: "You failed",
    },
    {
      type: "Exception",
      message: "Oh no exception",
    },
    {
      type: "CalledProcessError",
      message: "The second exception",
    },
  ]);

  // convert gRPC result to DB query
  let status;
  let output;

  if (result.type == "success") {
    output = result.user_code_output;
    if (result.solved) {
      status = SubmissionStatus.CORRECT;
    } else {
      status = SubmissionStatus.WRONG_ANSWER;
    }
  } else {
    status = SubmissionStatus.RUNTIME_ERROR;
    output = result.message;
  }

  const { userId, challengeId } = await prisma.submission.update({
    data: {
      status: status,
      output: output,
    },
    select: {
      userId: true,
      challengeId: true,
    },
    where: {
      id: submissionId,
    },
  });

  // update solve log
  if (status == SubmissionStatus.CORRECT) {
    await upsertSolveLog(userId, challengeId, submissionId);
  }

  console.log(`Finished grading submission ${submissionId}`);
}

main()
  .catch((e) => {
    console.log(e);
    throw e;
  })
  .finally(async () => {
    await prisma.disconnect();
  });
