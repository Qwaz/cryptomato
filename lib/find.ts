import {
  PrismaClient,
  ChallengeClient,
  ChallengeGetPayload,
  SubmissionGetPayload,
  FindManySubmissionArgs,
  ChallengeInclude,
  Subset,
} from "@prisma/client";

const prisma = new PrismaClient();

export function findChallengeWithStringId<T extends ChallengeInclude>(
  challengeId: string | string[],
  include?: T
): ChallengeClient<ChallengeGetPayload<{ include: T }> | null> {
  if (challengeId instanceof Array || !challengeId.match(/^[1-9]\d*$/)) {
    return null;
  }

  const challengeIdNumber = parseInt(challengeId);
  return prisma.challenge.findOne({
    where: {
      id: challengeIdNumber,
    },
    include,
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
