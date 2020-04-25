FROM node:14

WORKDIR /usr/app

RUN npm install --global pm2 cross-env

COPY ./package*.json ./
RUN npm install --production --no-package-lock
RUN npm install --save-dev typescript @types/react @types/node

COPY ./prisma ./prisma
RUN npm install --production --no-package-lock @prisma/client

COPY . ./
RUN rm -rf worker && mkdir worker
COPY ./worker/exposed_lib ./worker/exposed_lib
COPY ./worker/protos ./worker/protos

RUN npm run build

USER node
ENTRYPOINT ["pm2-runtime", "start", "npm", "--", "start"]
