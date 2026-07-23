FROM nginx:1.28-alpine

COPY gateway.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx","-g","daemon off;"]