FROM python:3.6
LABEL MAINTAINER="sj0225@icloud.com"

# 安装基础依赖软件，
COPY ./requirements.txt /
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 配置scrapyd
ADD scrapyd.conf /etc/scrapyd/scrapyd.conf

# 传入app应用文件，注意：src不含/，否则会丢失目录结构
RUN mkdir /app
COPY ./app /app/

EXPOSE 6800
VOLUME /app/logs

ENTRYPOINT ["/usr/local/bin/scrapyd"]