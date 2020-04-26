const { PrismaClient, SubmissionStatus } = require("@prisma/client");

// gRPC setup
const PROTO_PATH = __dirname + "/../cryptomato_worker/protos/private_api.proto";
const ENDPOINT_PATH =
  process.env.NODE_ENV === "production" ? "worker:10000" : "127.0.0.1:3001";

const grpc = require("grpc");
const protoLoader = require("@grpc/proto-loader");

const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
});
const package = grpc.loadPackageDefinition(packageDefinition);
const grpcClient = new package.Manager(
  ENDPOINT_PATH,
  grpc.credentials.createInsecure()
);

// start of the script
const prisma = new PrismaClient();
const submissionId = parseInt(process.argv[2]);

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
  const {
    code,
    userId,
    challenge: { id: challengeId, filename: challengeName },
  } = await prisma.submission.update({
    data: {
      status: SubmissionStatus.GRADING,
    },
    where: {
      id: submissionId,
    },
    select: {
      code: true,
      userId: true,
      challenge: {
        select: {
          id: true,
          filename: true,
        },
      },
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

  // invoke gRPC worker and get the result
  const payload = {
    challenge_name: challengeName,
    code: code,
  };
  grpcClient.evaluation(payload, async function (err, reply) {
    if (err) {
      // unknown error
      console.log(err);

      await prisma.submission.update({
        data: {
          status: SubmissionStatus.UNKNOWN_ERROR,
        },
        select: {
          id: true,
        },
        where: {
          id: submissionId,
        },
      });
    } else {
      // convert gRPC result to DB query
      let status;
      let output;
      let detail = null;

      const result = JSON.parse(reply.result);
      console.log(result);
      if (result.type === "success") {
        output = result.user_code_output;
        detail = JSON.stringify(result.detail);
        if (result.solved) {
          status = SubmissionStatus.CORRECT;
        } else {
          status = SubmissionStatus.WRONG_ANSWER;
        }
      } else {
        status = SubmissionStatus.RUNTIME_ERROR;
        output = result.message;
      }

      await prisma.submission.update({
        data: {
          status: status,
          output: output,
          detail,
        },
        select: {
          id: true,
        },
        where: {
          id: submissionId,
        },
      });

      // update solve log
      if (status == SubmissionStatus.CORRECT) {
        await upsertSolveLog(userId, challengeId, submissionId);
      }
    }

    console.log(`Finished grading submission ${submissionId}`);
    await prisma.disconnect();
  });
}

main().catch((e) => {
  console.log(e);
  throw e;
});
