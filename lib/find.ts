import { SubmissionGetPayload, FindManySubmissionArgs } from "@prisma/client";
import prisma from "./prisma";

type PotentialId = number | string | string[];

export function normalizeId(id: PotentialId): number | null {
  if (typeof id === "number") {
    return id;
  }

  if (id instanceof Array || !id.match(/^[1-9]\d*$/)) {
    return null;
  }

  return parseInt(id);
}

export const SerializableSubmissionSelect = {
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

export type SerializableCreatedAt<T> = Omit<T, "createdAt"> & {
  createdAt: string;
};

export type SerializableSubmission = SerializableCreatedAt<
  SubmissionGetPayload<{
    select: typeof SerializableSubmissionSelect;
  }>
>;

export function findSerializableSubmissions(
  args?: FindManySubmissionArgs
): Promise<Array<SerializableSubmission>> {
  return prisma.submission
    .findMany({
      ...args,
      select: SerializableSubmissionSelect,
    })
    .then((submissionArray) =>
      submissionArray.map((submission) => ({
        ...submission,
        createdAt: submission.createdAt.toLocaleString(),
      }))
    );
}
