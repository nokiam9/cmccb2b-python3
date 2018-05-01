# Ubuntu 14.04，Trusty Tahr（可靠的塔尔羊）发行版
#FROM daocloud.io/ubuntu:trusty
FROM ubuntu:14.04

MAINTAINER sj0225@icloud.com

# APT 自动安装 PHP 及其Extension的依赖包，如需其他依赖包在此添加
RUN apt-get update && \
    apt-get -y install curl wget unzip \
        apache2 libapache2-mod-php5 libpcre3-dev \
        php5-dev php5-mysql php5-sqlite php5-gd php5-curl && \
    apt-get -y install php-pear php-apc php-pear

    # 安装 Composer，此物是 PHP 用来管理依赖关系的工具
RUN curl -sS https://getcomposer.org/installer \
        | php -- --install-dir=/usr/local/bin --filename=composer && \

    # PHP 命令行的配置文件：//etc/php5/cli/php.ini，这是从pnp --ini的信息中找到"Loaded Configuration"字段
    # PHP 浏览器的配置文件：/etc/php5/apache2/php.ini，从浏览器打开phpinfo()中分析
    # 安装php-mongodb扩展, 并设置/etc/php5/cli/pnp.ini，注意两个都要安装
    pecl install mongodb && \
    echo "extension=mongodb.so" >> `php --ini | grep "Loaded Configuration" | sed -e "s|.*:\s*||"` && \
    echo "extension=mongodb.so" >> /etc/php5/apache2/php.ini && \

    # 调整 PHP 处理 Request 里变量提交值的顺序为EGPCS（ENV/GET/POST/COOKIE/SERVER），解析顺序从左到右，后解析新值覆盖旧值
    sed -i 's/variables_order.*/variables_order = "EGPCS"/g' \
        `php --ini | grep "Loaded Configuration" | sed -e "s|.*:\s*||"` && \

    # Apache2配置文件：/etc/apache2/apache2.conf，设置一个默认服务名，避免启动时给个提示让人紧张.
    echo "ServerName localhost" >> /etc/apache2/apache2.conf

# 安装xunsearch的PHP SDK组件
WORKDIR /usr/local/src
RUN wget "http://www.xunsearch.com/download/xunsearch-sdk-latest.zip"  && \
    unzip xunsearch-sdk-latest.zip -d ../xunsearch && \
    mv ../xunsearch/xunsearch-sdk ../xunsearch/sdk && \
    rm xunsearch-sdk-latest.zip

# 用完包管理器后安排打扫卫生可以显著的减少镜像大小, release发布时启用
RUN apt-get clean && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# PHP文件放入 /App目录
WORKDIR /
RUN mkdir -p /app && rm -rf /var/www/html && ln -s /app /var/www/html
COPY app/ /app

# xunsearch的项目文件放入SDK目录
COPY cmccb2b.ini /usr/local/xunsearch/sdk/php/app/

# 设置并运行docker的启动程序
COPY entrypoint.sh /
RUN chmod 755 ./entrypoint.sh

EXPOSE 80
CMD ["./entrypoint.sh"]
