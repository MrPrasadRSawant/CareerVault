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

RUN npm install -g @quasar/cli serve

COPY --from=build /app/dist/spa ./dist/spa

EXPOSE 9000

CMD ["serve", "-s", "./dist/spa", "-l", "9000"]
