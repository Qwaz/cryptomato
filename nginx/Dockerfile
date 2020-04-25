FROM nginx

RUN rm /etc/nginx/conf.d/*
COPY ./default.conf /etc/nginx/conf.d/
EXPOSE 8080
ENTRYPOINT ["nginx", "-g", "daemon off;"]
