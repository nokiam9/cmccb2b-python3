### 开发记录 v0.2 2018.03 ###
- 新增`.gitignore`, 避免git引入开发过程文件
- 新增`Workspace/`，用于一些临时测试和开发，通过后调整到正式文件
- 将`user_date/` 改名`UserDate/`，下一步考虑改为DB专用，
因为scrapy的log目录已经改为docker volume方式
- 修改`prestart.sh`，mongo支持docker-compose的override文件，
具体效果还需进一步研究
- 修改`setup.sh`，将mongo/migrations的样本数据该用管道处理，
避免文件解压，并将目录设为只读，以便控制GitHub的数据量



