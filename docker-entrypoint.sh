#!/bin/bash
set -e

DATABASE_PASSWORD=$(cat /run/secrets/database_password)
export DATABASE_URL="postgresql://cryptomato:$DATABASE_PASSWORD@database:5432/postgres?schema=cryptomato"
export SECRET_COOKIE_PASSWORD=$(cat /run/secrets/secret_cookie_password)

npx prisma migrate save --name init --experimental && npx prisma migrate up --experimental
npm run populate

exec "$@"
