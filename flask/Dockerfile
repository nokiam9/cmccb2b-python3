FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
LABEL MAINTAINER="sj0225@icloud.com"

ARG AppMajorVersion
ARG AppMinorVersion

# 安装依赖软件
WORKDIR /
COPY ./requirements.txt /
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 传入APP文件
COPY ./app_${AppMajorVersion}_${AppMinorVersion} /app

