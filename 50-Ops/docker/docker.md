#### 什么是Docker
**Docker 属于 Linux 容器的一种封装，提供简单易用的容器使用接口.它是目前流行的容器解决方案。

Docker 将应用程序与该程序的依赖，打包在一个文件里面。运行这个文件，就会生成一个虚拟容器。程序在这个虚拟容器里运行，就好像在真实的物理机上运行一样。有了 Docker，就不用担心环境问题。

Docker 的接口相当简单，用户可以方便地创建和使用容器，把自己的应用放入容器。容器还可以进行版本管理、复制、分享、修改，就像管理普通的代码一样。


#### Docker的用途
Docker 的主要用途，目前有三大类。00

（1）提供一次性的环境。比如，本地测试他人的软件、持续集成的时候提供单元测试和构建的环境。

（2）提供弹性的云服务。因为 Docker 容器可以随开随关，很适合动态扩容和缩容。

（3）组建微服务架构。通过多个容器，一台机器可以跑多个服务，因此在本机就可以模拟出微服务架构。
### docker-compose
Docker Compose是Docker编排服务的一部分，Compose可以让用户在集群中部署分布式应用。Docker Compose是一个属于“应用层”的服务，用户可以定义哪个容器组运行哪个应用，它支持动态改变应用，并在需要时扩展。通过编写合理的docker-compose.yml可以实现过个容器的快速部署


### docker和docker-compose安装脚本
```   
#!/bin/sh
# centos

#移除旧版本docker
yum remove docker \
    docker-client \
    docker-client-latest \
    docker-common \
    docker-latest \
    docker-latest-logrotate \
    docker-logrotate \
    docker-selinux \
    docker-engine-selinux \
    docker-engine

#安装一些必要的系统工具
yum install -y yum-utils device-mapper-persistent-data lvm2

#添加软件源信息
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo

#更新 yum 缓存
yum makecache fast

#安装 Docker-ce
yum -y install docker-ce

#启动 Docker 后台服务
systemctl start docker

#docker加入开机自启动
systemctl enable docker

//设置私有仓库地址
echo '{  "insecure-registries": ["仓库地址"] }
' > /etc/docker/daemon.json

systemctl daemon-reload
systemctl restart docker  或者   service docker restart 

#下载docket-compose
curl -L https://download.fastgit.org/docker/compose/releases/download/1.17.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose

#修改权限
chmod +x /usr/local/bin/docker-compose


 ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

```

```
1、更新`apt`包索引：

$ sudo apt-get update

2、允许`apt`通过HTTPS使用存储库来安装软件：

$ sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common

3、添加`Docker`官方 GPG 密钥：

$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

添加完成之后，使用下面命令进行验证秘钥，通过搜索指纹的最后8个字符，验证现在是否具有指纹`9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88`的密钥

$ sudo apt-key fingerprint 0EBFCD88

pub   rsa4096 2017-02-22 [SCEA]
      9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
uid           [ unknown] Docker Release (CE deb) <docker@docker.com>
sub   rsa4096 2017-02-22 [S]

4、使用下面的命令去设置稳定版的存储库。

$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

**安装 Docker CE**

1、更新`apt`包索引：

$ sudo apt-get update

2、安装最新版本的 `Docker CE` 和 `containerd`:

$ sudo apt-get install -y docker-ce docker-ce-cli containerd.io

3、验证`Docker`

使用下面的命令查看`Docker`的版本

$ docker -v

#下载docket-compose
curl -L https://download.fastgit.org/docker/compose/releases/download/1.17.1/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose

#修改权限
chmod +x /usr/local/bin/docker-compose

ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

```


#### docker使用
```
//拉取镜像 
docker pull [选项] [Docker Registry 地址[:端口号]/]仓库名[:标签]
docker pull gitlab/gitlab-ce:8.16.7-ce.0  

// 查看镜像
docker images

// 运行容器
docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]
例：
```shell
docker run \
-d \                    #容器在后台运行#
-p 20180:80 \           #指定端口映射#
-p 20122:22 \
--restart always \       #总是重启#
-v /data/gitlab/config:/etc/gitlab \     #指定容器卷#
-v /data/var/log/gitlab:/var/log/gitlab \
-v /data/gitlab/data:/var/opt/gitlab \
--name gitlab \                #命名#
gitlab/gitlab-ce:8.16.7-ce.0      #镜像名称#

// 进入运行中容器 
docker exec  -it gitlab /bin/bash

// 停止容器
docker stop gitlab

// 启动容器 
docker start gitlab 

```
#### docker镜像构建
镜像的定制实际上就是定制每一层所添加的配置、文件。如果我们可以把每一层修改、安装、构建、操作的命令都写入一个脚本，用这个脚本来构建、定制镜像，那么之前提及的无法重复的问题、镜像构建透明性的问题、体积的问题就都会解决。这个脚本就是 Dockerfile。
###### Dockerfile
示例:
```
FROM registry.cn-hangzhou.aliyuncs.com/aliyun-node/alinode:4.7.0-alpine

LABEL maintainer="zhangzheming<zhangzheming@cocheer.net>"

WORKDIR /data/app

ENV HOME /data/app

RUN apk --no-cache add python make g++

# 暴露端口
EXPOSE 3000

COPY package*.json ./
RUN npm install

# 拷贝应用程序
COPY ./. ./

# 运行命令
CMD [ "node", "bin/www.js" ]
```

指令详解
- FROM 
	指定基础镜像
- RUN 
	在镜像的构建过程中执行特定的命令，并生成一个中间镜像。比如安装一些软件、配置一些基础环境，可使用\来换行。
	`RUN <command> (shell格式)`
- WORKDIR
		为接下来的Dockerfile指令指定当前工作目录
- COPY
		将主机的文件复制到镜像内，如果目的位置不存在，Docker会自动创建所有需要的目录结构，但是它只是单纯的复制，并不会去做文件提取和解压工作。需要复制的目录一定要放在Dockerfile文件的同级目录下。
		`COPY <src>... <dest> COPY `
		`["<src>",... "<dest>"](路径包含空格的必须使用这种格式)`
- CMD 
	    指定容器运行时的默认参数。
	   `CMD ["executable","param1","param2"]（exec格式，首选）`
- EXPOSE 
		 为构建的镜像设置监听端口。
- ENV
		在构建的镜像中设置环境变量，在后续的Dockerfile指令中可以直接使用，也可以固化在镜像里，在容器运行时仍然有效。
- LABEL
		 `LABEL <key>=<value> <key>=<value> <key>=<value> ...`
		 如
		 `LABEL maintainer="zhangzheming<zhangzheming@cocheer.net>"`  添加维护者信息

编写镜像注意事项
-  **编写.dockerignore文件**
	构建镜像时，Docker需要先准备`context` ，将所有需要的文件收集到进程中。默认的`context`包含Dockerfile目录中的所有文件，但是实际上，**我们并不需要.git目录，node_modules目录等内容**。 `.dockerignore` 的作用和语法类似于 `.gitignore`，可以忽略一些不需要的文件，这样可以有效加快镜像构建时间，同时减少Docker镜像的大小

- **容器只运行单个应用**
	    一个容器部署一个应用，使用docker-compose关联多个应用
- **将多个RUN指令合并为一个，优先处理环境相关**
		Dockerfile中的每个指令都会创建一个新的镜像层。 镜像层将被缓存和复用，当Dockerfile的指令修改了，复制的文件变化了，或者构建镜像时指定的变量不同了，对应的镜像层缓存就会失效。某一层的镜像缓存失效之后，它之后的镜像层缓存都会失效。
		基于这个特性。我们尽量将一些不变动的部分单独编写。
		如上node环境示例：
		优先单独安装node的npm包，再拷贝项目文件。这样当代码变动时，npm包的缓存仍可使用。极大的节省了构建是npm包安装时间。
- **选择合适的基础镜像（alpine版本最好）**
		控制基础镜像大小

#### docker-compose 使用
```
docker-compose up -d  # 启动容器 -d 为设置后台运行

docker-compose down   # 停止容器
```

#### `docker-compose.yml`编写
示例：
```
version: '3.4'                            # 版本
services:                                 # 所有服务
  webmvc:                                 # 容器名称
	restart: always                       # 设置容器退出重启策略，always为总是重启
    image: eshop/webmvc                   # 容器镜像名称
    environment:                          # 设置容器环境变量，该变量可在容器中使用
      - CatalogUrl=http://catalog-api
      - OrderingUrl=http://ordering-api
      - BasketUrl=http://basket-api
    ports:                                # 端口映射
      - "5100:80"
    depends_on:                           # 依赖项，启动该容器前，会优先启动所依赖的容器
      - catalog-api
      - ordering-api
      - basket-api
	volumes:                         # 挂载数据卷，本机地址:容器内地址。可同步容器和本机文件
      - /home/zhexia/logs/cloud:/data/app/logs
  catalog-api:
    image: eshop/catalog-api
    expose:
      - "80"
    ports:
      - "5101:80"
    extra_hosts:
      - "CESARDLSURFBOOK:10.0.75.1"
    depends_on:
      - sqldata

  ordering-api:
    image: eshop/ordering-api
    ports:
      - "5102:80"
    #extra hosts can be used for standalone SQL Server or services at the dev PC
    extra_hosts:
      - "CESARDLSURFBOOK:10.0.75.1"
    depends_on:
      - sqldata

  basket-api:
    image: eshop/basket-api
    environment:
      - ConnectionString=sqldata
    ports:
      - "5103:80"
    depends_on:
      - sqldata

  sqldata:
    environment:
      - SA_PASSWORD=[PLACEHOLDER]
      - ACCEPT_EULA=Y
    ports:
      - "5434:1433"

  basketdata:
    image: redis

```


#### harbor介绍
Harbor，是一个英文单词，意思是港湾，港湾是干什么的呢，就是停放货物的，而货物呢，是装在集装箱中的，说到集装箱，就不得不提到Docker容器，因为docker容器的技术正是借鉴了集装箱的原理。所以，Harbor正是一个用于存储Docker镜像的企业级Registry服务。
Registry是Dcoker官方的一个私有仓库镜像，可以将本地的镜像打标签进行标记然后push到以Registry起的容器的私有仓库中。企业可以根据自己的需求，使用Dokcerfile生成自己的镜像，并推到私有仓库中，这样可以大大提高拉取镜像的效率。
#### Harbor和Registry的比较
Harbor和Registry都是Docker的镜像仓库，但是Harbor作为更多企业的选择，是因为相比较于Regisrty来说，它具有很多的优势。

1. 提供分层传输机制，优化网络传输 Docker镜像是是分层的，而如果每次传输都使用全量文件(所以用FTP的方式并不适合)，显然不经济。必须提供识别分层传输的机制，以层的UUID为标识，确定传输的对象。 
2. 提供WEB界面，优化用户体验 只用镜像的名字来进行上传下载显然很不方便，需要有一个用户界面可以支持登陆、搜索功能，包括区分公有、私有镜像。 
3. 支持水平扩展集群 当有用户对镜像的上传下载操作集中在某服务器，需要对相应的访问压力作分解。 
4. 良好的安全机制 企业中的开发团队有很多不同的职位，对于不同的职位人员，分配不同的权限，具有更好的安全性。 
5. Harbor提供了基于角色的访问控制机制，并通过项目来对镜像进行组织和访问权限的控制。kubernetes中通过namespace来对资源进行隔离，在企业级应用场景中，通过将两者进行结合可以有效将kubernetes使用的镜像资源进行管理和访问控制，增强镜像使用的安全性。尤其是在多租户场景下，可以通过租户、namespace和项目相结合的方式来实现对多租户镜像资源的管理和访问控制。

#### 安装harbor
通过docker安装

```
# 下载 harbor离线包
wget https://github.com/goharbor/harbor/releases/download/v2.3.2/harbor-offline-installer-v2.3.2.tgz

# 解压
tar xf harbor-offline-installer-v2.3.2.tgz

# 修改harbor配置文件
vim  harbor.yml   
修改hostname ，hostname为harbor的仓库地址

# 安装harbor

sudo ./prepare
sudo  ./install.sh

网页中输入修改的hostname则进入了harbor的后台管理页



docker 使用私有库需要配置

//设置私有仓库地址
echo '{  "insecure-registries": ["仓库地址"] }
' > /etc/docker/daemon.json

systemctl daemon-reload
systemctl restart docker  或者   service docker restart 

```