# Cryptomato

TODO: introduce project

## Development

### Local

First, set secret keys for local development.
Copy `next.config.js.example` to `next.config.js` and `prisma/.env.example` to `prisma/.env`
and change secret keys as you want.

Next, turn on local PostgreSQL container.
See `prisma/.env.example` file for the command.

Then, run a few initialization commands:

```shell
npm install
npx prisma generate
npx prisma migrate save --experimental
npx prisma migrate up --experimental
npm run populate
```

Then, build the worker image and run it.

```shell
bin/build.sh
docker run --rm --privileged --name cryptomato-worker -p 127.0.0.1:3001:10000 -d cryptomato_worker
```

Finally, run `npm run dev` to open a dev server at `localhost:3000`.

### Production

Run `bin/build.sh` and then `bin/run.sh`.

TODO: setup certificate
