***主要描述***
----------
xunsearch后台服务的安装点：`/usr/local/xunsearch`，其中：
-   `bin/`:后台服务的核心程序，包括`searchd`、`indexer`等
-   `data/`：索引文件的数据目录，将被mount到外部Volume
-   `etc/`：后台服务的配置文件，也包含自定义词典，但不含project文件
-   `include/`：后台服务是C++写的，这里是头文件
-   `lib/`：后台服务是C++写的，这里是库文件
-   `sdk/`：这也是PHP SDK的安装点，project配置文件也在这里
-   `share/`:还不清楚
-   `tmp/`:临时文件，存放pid和log等运行信息

xunsearch PHP SDK的安装点：`/usr/local/xunsearch/sdk/php`，其中：
- `app/`: 存放核心的项目配置文件`cmccb2b.ini`和`demo.ini`
- `lib/`: php lib库文件
- `util/`: 一些实用脚本程序
- `doc/`: 文档资料

前台UI界面在：`docker/php:/app`，其中：
- `search.php `:搜索的主入口，Usage：`0.0.0.0:9000/search.php`
- `suggest.php`: 提供搜索建议的页面
- `search.tpl`: PHP定义的模版文件
- `css/`: 样式表
- `img/`: 图像文件

**注意：每个php脚本都需要包含xunsearch定义的lib文件：`require_once '/usr/local/xunsearch/sdk/php/lib/XS.php';`**

--------
### 参考文档 ###
- [xunsearch的下载地址](http://www.xunsearch.com/site/download)  
- [xunsearch的参考文档](http://www.xunsearch.com/doc/php/guide/start.overview)