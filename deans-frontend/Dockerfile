# Stage 1: Build
FROM node:18-alpine as builder

WORKDIR /work

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# Stage 2: Runtime
FROM node:18-alpine

WORKDIR /work

# Install serve to run the app
RUN npm install -g serve

COPY --from=builder /work/package.json .
COPY --from=builder /work/node_modules ./node_modules
COPY --from=builder /work/build ./build

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000 || exit 1

CMD ["serve", "-s", "build", "-l", "3000"]