# Docker crontab from dockerd（daemon docker）

## 功能概述

- 基础镜像：[library/docker:stable](https://github.com/docker-library/docker) ,支持基于[docker for docker](https://docs.docker.com/edge/engine/reference/commandline/dockerd/)的自定义crontab调用
- 生成镜像:`nokiam9/crontab`，补充安装curl用于scrapyd的http调用（本应用没有使用image && container）
- 启用本容器需要加载`/var/run/docker.sock`（宿主机的套接字）和`config.json`(以json格式描述的定时任务清单)
- 启动方式:`docker-compose up -d --build`

------

## 经验之谈

- docker in docker的原理是在container通过socket的套接字通信，将指令转发给宿主机的2375监听端口，并执行docker命令，详见[参考文档](https://zhuanlan.zhihu.com/p/26413099)
- 定时任务的模版定义`config.sample.json`，既支持传统的`* * * * *`方式，也支持`@hourly`或`every 2m`的表达方式
- alpine是docker的默认原始镜像，文件size只有5M，而且支持[apk软件包管理](http://wiki.alpinelinux.org/wiki/Alpine_Linux_package_management)，方法类似于apt

- container启动后一般需要进入后台程序，否则command结束后进入Exit状态,多次启动后遗留一大批Exit的container（手工清理方式：`docker container prune`）
- docker for docker的软件包安装目录：`/usr/local/bin`

------

## 遗留问题

- 需要进一步研究跨compose文件的集成方法