#!/bin/bash
set -e

chown root:node prisma/migrations && chmod 770 prisma/migrations

DATABASE_PASSWORD=$(cat /run/secrets/database_password)
export DATABASE_URL="postgresql://cryptomato:$DATABASE_PASSWORD@database:5432/postgres?schema=cryptomato"
export SECRET_COOKIE_PASSWORD=$(cat /run/secrets/secret_cookie_password)

export USER=node
export HOME=/home/node

su --preserve-environment -c 'npx prisma migrate save --name init --experimental' node
su --preserve-environment -c 'npx prisma migrate up --experimental' node
su --preserve-environment -c 'npm run populate' node

ARGV=$@
exec su --preserve-environment -c "exec $ARGV" node
