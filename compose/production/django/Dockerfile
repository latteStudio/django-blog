FROM python:3.6-apline

ENV PYTHONUNBUFFERED 1

RUN apk update \
# pillow dependencies
    && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

# django处理图片需要Pillow库

WORKDIR /app

RUN pip install pipenv -i https://pypi.douban.com/simple
# 指定工作目录，下载pipenv库

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
RUN  pipenv install --system --deploy --ignore-pipfile
# 本地的依赖文件目录拷贝到容器中，并下载依赖 --system安装到系统级别，即镜像级别，因为容器中不需要再来虚拟环境了


COPY . /app
# 把项目根目录下，所有除了.dockerignore的文件，都拷贝到容器的/app下，（即项目代码，静态文件只目录把？

COPY ./compose/production/django/start.sh /start.sh
# 容器的启动脚本

RUN sed -i 's/\r//' /start.sh
# 去除windows系统下的\r

RUN chmod +x /start.sh


