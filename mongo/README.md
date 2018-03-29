## Mongo Docker ##

主要功能：以container方式启动mongo 3.6，并提供27017端口访问  
加载方式: `sh prestart.sh` ，其中加载了`mongo.yml` ，本地开发环境还加载了 `mongo.override.yml`  
卸载方式: 不需要，或者手工执行`docker stop mongo`

### 参考文档 ###
- [Mongo Shell](https://docs.mongodb.com/manual/mongo/)
- [Pymongo/3.6](http://api.mongodb.com/python/current/index.html)
- [MongoEngine](http://docs.mongoengine.org/index.html)
- [Docker for mongo/3.6](https://github.com/docker-library/mongo/tree/a504b49bb5cf896fbf3640b4b8cb0d09a25b53ae/3.6)
- [docker-compose v2参考手册](https://docs.docker.com/compose/compose-file/compose-file-v2/)


### 注意事项 ### 
- 建议启动使用-d参数，后台方式启动，无需人工干预
- container的name已经固定为mongo，便于测试
- `../data/db`是数据库的数据文件目录，`../data/configdb`是数据库集群的默认设置，单节点时为空目录
- 自定义加载`../data/migrations`用于数据迁移，网络传输文件速度慢时建议gzip压缩  
            
```
# 从mongon导出表数据
mongoexport -d cmccb2b -c Cmccb2bItem -o Cmccb2bItem.json
# 将json格式的数据导入mongo
mongoimport -d cmccb2b -c Cmccb2bItem --drop < Cmccb2bItem.json
```
            
- 自定义加载`../data/scripts`用于数据测试，例如在mongo容器内使用以下命令可以查看每天新发布的招标信息

```
# 进入mongo容器
docker exec -it mongo /bin/bash
# 在容器内调用mongo客户端，并启动脚本文件
mongo < group_by_crawled_time.js
```


