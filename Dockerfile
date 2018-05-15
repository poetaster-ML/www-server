from node:8.9.4-alpine

WORKDIR app

COPY ./ .

RUN yarn install
