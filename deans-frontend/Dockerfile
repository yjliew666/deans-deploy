# Link to Repository: https://github.com/yjliew666/deans-deploy
# Source: deans-frontend/Dockerfile
FROM node:10
WORKDIR /work
COPY package.json ./
RUN yarn install --ignore-engines
COPY . .

EXPOSE 3000

CMD ["yarn", "start"]