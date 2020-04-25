FROM node:14

WORKDIR /usr/app

RUN npm install --global pm2 cross-env

COPY ./package*.json ./
RUN npm install --production --no-package-lock
RUN npm install --save-dev typescript @types/react @types/node

COPY ./prisma ./prisma
RUN npx prisma generate
VOLUME /usr/app/prisma/migrations

COPY . ./
RUN rm -rf worker && mkdir worker
COPY ./worker/exposed_lib ./worker/exposed_lib
COPY ./worker/protos ./worker/protos

RUN npm run build

COPY docker-entrypoint.sh /usr/local/bin/
RUN ln -s /usr/local/bin/docker-entrypoint.sh /

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["pm2-runtime", "start", "npm", "--", "start"]
