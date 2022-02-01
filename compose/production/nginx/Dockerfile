FROM nginx:1.17.1

# 替换国内源
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
COPY ./compose/production/nginx/sources.list /etc/apt/
RUN apt-get update && apt-get install -y --allow-unauthenticated certbot python-certbot-nginx

# 拷贝项目的nginx配置
RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/production/nginx/django-blog.conf /etc/nginx/conf.d/django-blog.conf


