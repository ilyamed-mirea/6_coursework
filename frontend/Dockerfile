FROM node:lts
WORKDIR /app

COPY . .

RUN npm ci
RUN npm run build

ENV HOST=0.0.0.0
ENV PORT=4321
CMD node ./dist/server/entry.mjs