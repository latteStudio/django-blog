# 指定基础镜像
FROM python:3.6-alpine
ENV PYTHONUNBUFFERED 1

# 下载django需要的依赖：apk-先替换源，
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories  && apk update \
# pillow dependencies
    && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
# django处理图片需要Pillow库

# 指定工作目录
WORKDIR /app


# 拷贝Pipfile2个
COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
RUN  pip install pipenv -i https://pypi.douban.com/simple
RUN  pipenv install --system --deploy --ignore-pipfile
# 修改pip的源、先下载pipenv --system级别：根据Pipfile下载依赖

# 拷贝start.sh脚本，注意linux系统的换行符、添加执行权限
COPY ./compose/local/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

