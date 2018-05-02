FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
LABEL MAINTAINER="sj0225@icloud.com"

ARG AppMajorVersion
ARG AppMinorVersion

# 安装依赖软件
WORKDIR /
COPY ./requirements.txt /
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装nginx的配置文件，支持https和部分站点重定向
COPY nginx/ssl/caogo.cn.crt /etc/nginx/ssl/caogo.cn.crt
COPY nginx/ssl/caogo.cn.key /etc/nginx/ssl/caogo.cn.key

COPY nginx/scrapyd_proxy.conf /etc/nginx/conf.d/
COPY nginx/ssl.conf /etc/nginx/conf.d/

# 传入APP文件
COPY ./app_${AppMajorVersion}_${AppMinorVersion} /app

