import {
  PrismaClient,
  ChallengeClient,
  ChallengeGetPayload,
  SubmissionGetPayload,
  FindManySubmissionArgs,
} from "@prisma/client";

const prisma = new PrismaClient();

export type ChallengeWithCategories = ChallengeGetPayload<{
  include: {
    categories: true;
  };
}>;

export function findChallengeWithStringId(
  challengeId: string | string[]
): ChallengeClient<ChallengeWithCategories | null> {
  if (challengeId instanceof Array || !challengeId.match(/^[1-9]\d*$/)) {
    return null;
  }

  const challengeIdNumber = parseInt(challengeId);
  return prisma.challenge.findOne({
    where: {
      id: challengeIdNumber,
    },
    include: {
      categories: true,
    },
  });
}

export const SubmissionListSelect = {
  id: true,
  challenge: {
    select: {
      id: true,
      name: true,
    },
  },
  user: {
    select: {
      id: true,
      nickname: true,
    },
  },
  createdAt: true,
  status: true,
};

export type SerializableSubmissionListElem = Omit<
  SubmissionGetPayload<{
    select: typeof SubmissionListSelect;
  }>,
  "createdAt"
> & { createdAt: string };

export function findSerializableSubmissions(
  args?: FindManySubmissionArgs
): Promise<Array<SerializableSubmissionListElem>> {
  return prisma.submission
    .findMany({
      ...args,
      select: SubmissionListSelect,
    })
    .then((submissionArray) =>
      submissionArray.map((submission) => ({
        ...submission,
        createdAt: submission.createdAt.toLocaleString(),
      }))
    );
}
