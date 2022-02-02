#!/bin/sh


python manage.py migrate
python manage.py collectstatic --noinput
# 容器内部不拷贝代码，数据库文件、静态文件，靠挂载：宿主机的目录（实现宿主机修改，即可实现变更——开发阶段，需频繁修改）

python manage.py runserver 0.0.0.0:8000