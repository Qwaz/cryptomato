FROM node:lts

WORKDIR /usr/app

RUN npm install --global pm2 cross-env

COPY ./package*.json ./
RUN npm install --production --no-package-lock
RUN npm install --save-dev typescript @types/react @types/node

COPY ./prisma ./prisma
RUN npx prisma generate
RUN mkdir prisma/migrations && chown root:node prisma/migrations && chmod 770 prisma/migrations

COPY . ./
RUN rm -rf cryptomato_worker && mkdir cryptomato_worker
COPY ./cryptomato_worker/exposed_lib ./cryptomato_worker/exposed_lib
COPY ./cryptomato_worker/protos ./cryptomato_worker/protos
COPY ./cryptomato_worker/challenges ./cryptomato_worker/challenges

RUN SECRET_COOKIE_PASSWORD=$(cat ./secrets/secret_cookie_password.txt) npm run build && rm -rf secrets

COPY docker-entrypoint.sh /usr/local/bin/
RUN ln -s /usr/local/bin/docker-entrypoint.sh /

USER node
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["pm2-runtime", "start", "npm", "--", "start"]
