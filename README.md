# cmccb2b Package Based on Python3.6

## 安装方式（基于GitHub）

1. 将本地开发环境上传GitHub
2. 生产机（已安装docker，python3.6不是必须的）下载clone源代码`git clone xxxx`，并改名为`/app`
3. 新建`/data`数据目录及子目录`db/`，`xunsearch/`，可以用migration脚本迁移mongo DB数据（可选）
4. 启动预安装程序`sh prestart.sh`，并启动主程序`docker-compose up -d --build`
5. 浏览器远程访问<www.caogo.cn>

### 核心应用目录

- `nginx/`: 站点主入口，分别导流至scrapy、flask、xunsearch，并支持https和http重定向
- `scrapy/`：后台scrapy应用，运行环境集成了scrapyd(:6800)和scrapy_client，其中`app/`存放python应用
- `falsk/`：前台flask应用，运行环境集成了uWSGI和nginx，其中`app/`存放python应用
- `xunsearch/`: 中文搜索引擎，运行环境包括后台server和前台php(:9000)，其中`app/`存放php应用
- `mongo/`：公共数据库应用，其中`migarion/`包含样本数据和数据库迁移脚本，`scripts/`包含应用系护的一些脚本，如数据转换
- `crontab/`：后台定时任务调度，为scrapy提供服务，运行环境集成了docker for docker
- `/data`:用户数据目录，包括db、xunsearch等，注意VCS和GitHub不包含该目录。</font>  
- `prestart.sh`: 预启动程序，负责设置network并启动mongo，*注意：本地开发测试增加-dev参数，提供mongodb外部访问*
- `docker-compose.yml`:主启动程序，自动加载scrapy、flask、xunsearch和crontab等全部容器

#### 开发辅助目录

- `worksapce/`:临时工作目录，初步开发的程序，不含在Git管理范围
- `venv/`:python3.6的虚拟环境
- `.gitignore`：设置不需要上传Github的文件类型
- `setup.shell`：生产环境的安装示例文件
- `README-python2.md`：基于python2.7的自述文件
- `README.md`: 本文件

### 注意事项

- 数据目录/data不在/app中，需要手工创建并建立子目录db/，xunsearch/
- xunsearch的index独立于mongo，清除方法为：`docker exec -it xunsearch php /app/xs_clean_index.php` 或者直接清除`/data/xunsearch`
- 由于GitHub上已经用过cmccb2b的name，因此改名为cmccb2b_package
- ECS生产环境docker版本低，version＝2

### 安装方式（tar方式，已废弃）

1. 在上层目录将全部文件打包`tar -cvf app.tar CMCCB2B`
2. scp到生产机（已安装docker）并在安装点解包`tar -xvf app.tar`
3. 如果需要，调整user_data的目录设置，或迁移mongo DB数据
4. 启动预安装程序`sh prestart.sh`，并启动主程序`docker-compose up -d --build`
5. 浏览器远程访问[www.caogo.cn](www.caogo.cn)