### cmccb2b Package Based on Python3.6 ###

### 安装方式（基于GitHub） ###
1. 将本地开发环境上传GitHub
2. 生产机（已安装docker，python3.6）并在安装clone源代码`git clone xxxx`
3. 新建`data/`数据目录，并用migration脚本迁移mongo DB数据
4. 启动预安装程序`sh prestart.sh`，并启动主程序`docker-compose up -d --build`
5. 浏览器远程访问<www.caogo.cn>  或者 <a href="http://47.52.226.119">47.52.226.119</a>  

### 文件清单 ###
- `scrapy/`：后台scrapy应用，运行环境集成了scrapyd和scrapy_client，其中`app_?_?/`存放app各个版本(version: major+minor)
- `falsk/`：前台flask应用，运行环境集成了uWSGI和nginx，其中`app_?_?/`存放app各个版本 
- `mongo/`：公共数据库应用，其中`migarion/`包含样本数据和数据库迁移脚本，`scripts/`包含应用系护的一些脚本，如数据检查等。
- `crontab/`：后台定时任务调度，为scrapy提供服务，运行环境集成了docker for docker
- `worksapce/`:临时工作目录，初步开发的程序，不含在Git管理范围
- `data`:<font color="orange">用户数据，包括db、logs等，注意VCS和GitHub不包含该目录。</font>
- `prestart.sh`: 预启动程序，负责设置network并启动mongo，*注意：在启动docker-compose前，必须运行该程序*
- `docker-compose.yml`:主启动程序，自动加载scrapy，flask和crontab容器
- `.gitignore`：设置不需要上传Github的文件类型
- `setup.shell`：生产环境的安装示例文件
- `README-python2.md`：基于python2.7的自述文件
- `README.md`: 本文件


### 注意事项 ###
- GitHub上传不含`user_date/`目录，需要手工设置yml文件中的volume
- 由于GitHub上已经用过cmccb2b的name，因此改名为cmccb2b_package
- ECS生产环境docker版本低，version＝2
- 考虑scrapy:6800关闭外网访问，取消首页链接


### 安装方式（tar方式，已废弃） ###
1. 在上层目录将全部文件打包`tar -cvf app.tar CMCCB2B`
2. scp到生产机（已安装docker）并在安装点解包`tar -xvf app.tar`
3. <font color="orange">如果需要，调整user_data的目录设置，或迁移mongo DB数据</font>
4. 启动预安装程序`sh prestart.sh`，并启动主程序`docker-compose up -d --build`
5. 浏览器远程访问<www.caogo.cn>  或者 <a href="http://47.52.226.119">47.52.226.119</a>  

