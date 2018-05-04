FROM willfarrell/crontab
LABEL MAINTAINER="sj0225@icloud.com"

# install curl for docker:scrapyd
RUN apk update && apk add --virtual .run-deps curl

# 传入config配置文件
COPY config.json /opt/crontab/
