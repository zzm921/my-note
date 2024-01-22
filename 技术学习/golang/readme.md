#### 项目介绍
该项目为简单选举系统，采用 goframe进行后端接口编写，使用mysql作为数据库，redis作为缓存。
项目提供后台管理员登录接口，登录后可进行候选人录入修改，选举录入，选举状态修改，查看选举状态等功能。为用户提供查看选举信息、投票功能。

#### 项目运行
1. 安装`go`和`goframe`环境
可参考`https://goframe.org/pages/viewpage.action?pageId=1114399`
2. 下载项目
`git clone git@github.com:zzm921/election-go.git`
3. 创建数据库
运行项目中sql文件 `manifest\sql\Dump20221020.sql` 创建数据库表
4. 运行项目
使用命令
`gf run main.exe`   
开发过程中可使用vscode等工具的调试模式启动
5. 编译项目
使用`gf build`可根据`hack\config.yaml`中配置的编译配置编译项目。生成可执行文件。
6. 打包项目
项目可采用docker的形式部署，可使用命令
` gf docker main.go  -tn youDockerHub/election:test` 将程序打包成镜像，
或者根据`manifest\docker\Dockerfile`文件使用`docker build`命令将程序打包成镜像
7. 部署项目
服务器拉取docker镜像。使用命令后台启动容器
`docker run -itd -p 8000:8000 --name election youDockerHub/election:test`

#### 项目目录及说明
##### 项目配置
项目配置文件`manifest\config\config.yaml` 配置文件配置项目，mysql，redis等信息.使用时需改为自己的mysql，redis地址

##### 接口定义
接口注册文件位于`api`目录下，由于该项目采用了规范路由注册方式，因此在API结构体的属性中包含一些标签。其中结构体属性的`v`标签表示校验规则，请求参数进入`HTTP Server`后将会被自动执行校验

##### 路由注册
路由注册在`cmd`包中，在本项目中，仍旧采用灵活的分组路由注册方式。在不分路由中带有鉴权中间件，这部分路由需要鉴权后才能访问。

##### 常量管理
项目的所有常量位于`internal/consts`包下，供项目所有的包全局访问，常量通过不同的文件及名称命名前缀来区分不同的业务模块。

##### 控制器定义
控制器在`internal\controller`目录下，控制器往往不带有任何的业务逻辑，负责API接口数据结构的输入与输出，调用一个或多个`service`实现具体的业务逻辑。

##### 业务模型
业务模型在`internal\model`目录下定义,业务项目中内部模块间交互的数据结构由`model`包维护，供全局访问。


##### 服务接口
为了降低业务项目内部模块间的耦合，框架将模块间的依赖抽象为了接口，由`internal/service`包维护。通过`internal/logic`业务封装的代码按照一定规则自动生成接口代码文件。
使用命令`gf gen service` 根据`internal/logic`中的业务代码,自动生成service文件。

##### 业务实现
业务的具体实现由`internal/logic`包维护，通过依赖注入的方式注册具体的实现对象到`internal/service`包下。

##### dao代码生成
通过`gf gen dao`可根据在`hack\config.yaml`中配置的数据库表信息，自动生成dao代码。

##### 接口文档
项目接口文档使用swagger。启动项目后，输入`localhost:8000/swagger`可查看项目的接口文档

#### 部分流程说明
##### 账号登录密码
登录密码传输前端需使用aes加密。加密后数据传入后端。后端通过对应的aes解密获取用户密码。
账号密码使用加盐md5存储。
##### 账号登录校验
账号登录使用token存储的方式，登录成功后通过一定规则生成token，将token存入redis中。为浏览器设置cookie。
请求通过中间件检测token是否存在来判断是否登录
##### 邮件发送
邮件发送使用三方邮件包。使用时需改为自身的邮箱配置
使用go协程池时间邮件群发

#### 接口使用说明
详细接口文档见`localhost:8000/swagger`.

接口列表说明
| 接口             | 说明                             | 地址                                                         |
| ---------------- | -------------------------------- | ------------------------------------------------------------ |
| 账号登录         | 登录后台                         | get `/crm/account/login`                                     |
| 候选人创建       | 创建候选人信息                   | post `/crm/candidate`                                        |
| 候选人更新       | 更新候选人信息                   | put `/crm/candidate/:CandidateId`                            |
| 候选人获取       | 获取候选人信息                   | get   `/crm/candidate`                                       |
| 选举创建         | 创建选举                         | post /crm/election                                           |
| 选举更新状态     | 更新选举状态(开始或结束)         | put  `/crm/election/:ElectionId/status`                      |
| 选举查看         | 查看所有的选举                   | get   `/crm/election`                                        |
| 选举候选人查看   | 产看参与选举的候选人信息得票数等 | get `/crm/election/:ElectionId/candidates/:CandidateId/vote` |
| 用户获取当前选举 | 查看当前进行中的选举             | get `/user/election  `                                       |
| 用户投票         | 用户选举投票                     | post `/user/vote`                                                             |
