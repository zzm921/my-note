####基础概念

Redis 是完全开源免费的，遵守BSD协议，是一个高性能的key-value数据库。

Redis 与其他 key - value 缓存产品有以下三个特点：

- Redis支持数据的持久化，可以将内存中的数据保存在磁盘中，重启的时候可以再次加载进行使用

- Redis不仅仅支持简单的key-value类型的数据，同时还提供list，set，zset，hash等数据结构的存储。

- Redis支持数据的备份，即master-slave模式的数据备份。
####安装
- centos ： yum   install   redis
- ubuntu :apt-get intstall redis
####运行
- 启动：redis-server
- 查看： ps   -ef |   grep   redis
####设置开机自启动
- chkconfig redis on

####连接
- redis-cli 
- redis-cli -h host -p port -a password
####