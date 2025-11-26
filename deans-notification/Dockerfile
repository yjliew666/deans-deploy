# FROM nginx:1.15.2-alpine
# # you have to build before copy
# COPY ./dist /var/www
# COPY nginx.conf /etc/nginx/nginx.conf
# EXPOSE 80
# ENTRYPOINT ["nginx","-g","daemon off;"]

FROM node:8.11.1
# you have to build before copy
COPY . /var/www
WORKDIR /var/www
RUN yarn install
RUN yarn build
# RUN yarn start
# EXPOSE 80
# ENTRYPOINT ["yarn","start"]