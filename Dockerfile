# Link to repository
# Repository: https://github.com/yjliew666/deans-deploy/tree/feature-integrated
FROM node:10-alpine
WORKDIR /app
RUN apk add --no-cache python make g++
COPY deans-frontend/package.json ./
RUN yarn install --ignore-engines
COPY deans-frontend/ .

EXPOSE 3000

CMD ["yarn", "start"]