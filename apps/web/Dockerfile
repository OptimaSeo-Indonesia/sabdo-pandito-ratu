FROM node:20-alpine

WORKDIR /app

COPY apps/web/package.json apps/web/pnpm-lock.yaml* ./
RUN corepack enable && pnpm install

COPY apps/web/ .

EXPOSE 3000

CMD ["pnpm", "dev"]
