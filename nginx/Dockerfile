FROM nginx:1.21-alpine

ARG PORT
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
RUN sed -i s/PORT/$PORT/g /etc/nginx/conf.d/nginx.conf
