FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
LABEL MAINTAINER="sj0225@icloud.com"

# 安装基础依赖软件
WORKDIR /
COPY ./requirements.txt /
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 传入APP文件，注意：src不含／，必须整个目录拷贝
COPY ./app /app

