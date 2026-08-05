# build stage
FROM node:24-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# runtime stage
FROM node:24-alpine

WORKDIR /app
ENV NODE_ENV=production

RUN npm install -g @quasar/cli

COPY --from=build /app/dist/spa ./dist/spa

EXPOSE 9000

CMD ["quasar", "serve", "./dist/spa", "--port", "9000", "--history"]