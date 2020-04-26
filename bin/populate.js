const fs = require("fs");
const { PrismaClient } = require("@prisma/client");
const toml = require("toml");

const prisma = new PrismaClient();

const addCategory = async (name) => {
  const result = await prisma.category.upsert({
    create: {
      name: name,
    },
    update: {},
    where: {
      name: name,
    },
  });
  return result.id;
};

const addChallenge = async (name, description, level, categoryId) => {
  const categoryIdConnect = categoryId.map((id) => {
    return {
      id: id,
    };
  });

  const result = await prisma.challenge.upsert({
    create: {
      name: name,
      description: description,
      level: level,
      categories: {
        connect: categoryIdConnect,
      },
    },
    update: {
      description: description,
      level: level,
      categories: {
        connect: categoryIdConnect,
      },
    },
    where: {
      name: name,
    },
  });

  return result;
};

const CHALLENGE_DIR = "cryptomato_worker/challenges";

async function main() {
  for (const filename of fs.readdirSync(CHALLENGE_DIR)) {
    if(!filename.endsWith(".toml")) continue;

    console.log(`Processing ${filename}`);
    const data = fs.readFileSync(`${CHALLENGE_DIR}/${filename}`);
    let content = toml.parse(data);

    const categoryIdArr = [];
    for (const category of content.categories) {
      const categoryId = await addCategory(category);
      categoryIdArr.push(categoryId);
    }

    await addChallenge(
      content.name,
      content.description,
      content.level,
      categoryIdArr
    );
  }
}

main()
  .catch((e) => {
    console.log(e);
    throw e;
  })
  .finally(async () => {
    await prisma.disconnect();
  });
