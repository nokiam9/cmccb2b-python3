FROM nginx:1.12.2
LABEL MAINTAINER="sj0225@icloud.com"

# 安装支持https的自定义SSL证书
COPY ssl/caogo.cn.crt /etc/nginx/ssl/caogo.cn.crt
COPY ssl/caogo.cn.key /etc/nginx/ssl/caogo.cn.key

# 替换nginx的配置文件
COPY default.conf /etc/nginx/conf.d/
