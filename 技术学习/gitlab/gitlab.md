#### 安装gitlab
```
sudo apt-get install curl openssh-server ca-certificates postfix

curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash

sudo apt-get install gitlab-ce

```
修改 gitlab 的配置文件 `/etc/gitlab/gitlab.rb`,修改extract_url

修改完成配置之后使用 `gitlab-ctl reconfigure` 重新更新一下 gitlab 服务的配置，更新完成配置之后使用  
`gitlab-ctl restart` 来重新启动 gitlab 。如果 reconfigure 失败，则需要 `systemctl enable gitlab- runsvdir && systemctl restart gitlab- runsvdir` 重启一下 `gitlab-runsvdir` 服务。

打开浏览器进行初始化账户设定密码，这个密码为 root 管理员账户的密码。设置完密码之后会自动跳转到登录页面。username 为 `root` 密码为刚刚设置的密码。

### 安装gitlab-runner
```
//更新源
curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash

//安装
sudo apt-get install gitlab-runner


```


### 注册gitlab-runner
```
gitlab-runner register
# 去gitlab中可以看到对应的runner对应的地址和token，根据需求注册不同的runner

根据文档提示按照步骤注册gitlab-runner

1.  输入gitlab的服务URL ，在gitlab中可以查看
    
2.  输入gitlab-ci的token，获取在项目当中的settings中的子菜单CI/CD 中的Runners Tab模块
    
3.  关于集成服务中对于这个runner的描述
    
4.  给这个gitlab-runner输入一个标记，这个tag非常重要，在后续的使用过程中需要使用这个tag来指定gitlab-runner
    
5.  是否运行在没有tag的build上面。在配置gitlab-ci的时候，会有很多job，每个job可以通过tags属性来选择runner。这里为true表示如果job没有配置tags，也执行
    
6.  是否锁定runner到当前项目
    
7.  选择执行器，shell,docker,等

```

一般使用docker作为执行器时，需要更改runner配置
```
sudo vim  /etc/gitlab-runner/config.toml

修改
 privileged = ture
 volumes = ["/var/run/docker.sock:/var/run/docker.sock"]


重启gitlab-runner
sudo gitlab-runner restart

```


#### gitlab-ci/cd使用
##### `gitlab-ci.yml` 详解,如：
```
# docker镜像
image: node
# 依赖的docker服务
services:
  - postgres
# 开始执行脚本前所需执行脚本
before_script:
  - bundle install
# 脚本执行完后的钩子，执行所需脚本
after_script:
  - rm secrets
# 该ci pipeline适合的场景
stages:
  - build
  - test
  - deploy
# 定义的任务1
job1:
  # 场景为构建
  stage: build
  # 所需执行的脚本
  script:
    - execute-script-for-job1
  # 在哪个分支上可用
  only:
    - master
  # 指定哪个ci runner跑该工作
  tags:
    - docker
```
##### 配置项说明
###### image and services 
这两个选项允许我们指定任务运行时所需的自定义的docker镜像服务。


###### before_script
**before_script**是用于定义一些在所有任务执行前所需执行的命令, 包括部署工作（但是是在job环境手动恢复之后执行）。可以接受一个数组或者多行字符串。


###### after_script
**after_script**用于定义所有job执行过后需要执行的命令. 可以接受一个数组或者多行字符串。

> **注意:** **before_script**和**script**在一个上下文中是串行执行的，**after_script**是独立执行的，所以根据执行器(在runner注册的时候，可以选择执行器，docker,shell,blabla...)的不同，工作树之外的变化可能不可见，例如，在before_script中执行软件的安装。
> 
> 注意:你可以在任务中定义before_script，after_script，也可以将其定义为顶级元素，定义为顶级元素将为每一个任务都执行相应阶段的脚本或命令


###### stages
**stages**是用于定义场景阶段，可以被任务所使用用于定义所属场景阶段。stages的允许定义多个，灵活的场景阶段的pipline。

stages定义的元素的顺序决定了任务执行的顺序:

1.任务指定的stage名相同，该多个任务将并行执行(但是经过测试，貌似也是按照A-Z的头字母顺序顺序执行的。。只是GitLab-UI上看着是并行。。。)  
2.下一个场景阶段的任务将会在前一个场景阶段的任务都完成的情况下执行

让我们来思考一下下面的例子，下面的例子定义了3个场景阶段:

stages:
  - build
  - test
  - deploy

1.首先, 所有build场景的任务将被并行执行.  
2.如果所有build场景的任务都成功了, test场景的所有任务将会并行执行.  
3.如果所有test场景的任务都成功了, depoly场景的所有任务将会执行.  
4.如果所有depoly场景的任务都成功了, 提交将会标记为成功.  
5.如果其中某一步场景某一个任务失败了, 那么提交将会被标记为失败，并且之后的场景和任务将不会执行.

这里也有两种边缘情况值得一说：

1.  如果在.gitlab-ci.yml中没有定义stages,build、test、deploy将是任务可设定的场景阶段的默认值.
2.  如果一个任务没有指定场景阶段，该任务将会默认为test场景阶段，

###### script
**script**是一段由Runner执行的shell脚本，例如：

job:
  script: "bundle exec rspec"

这个参数也可以使用数组包涵好几条命令：

job:
  script:
    - uname -a
    - bundle exec rspec

有些时候，**script**命令需要被单引号或者双引号所包裹。举个例子，命令中包涵冒号的时候，该命令需要被引号所包裹，这样YAML解析器才知道该命令语句不是“key: value”语法的一部分。当命令中包涵以下字符时需要注意打引号:**:** { } [] , **&** ***** **#** **?** **|** **-** **<** **>** **=** **!** **%** **@**


###### stage
**stage**指定一组job在不同场景阶段执行。在相同**stage**下的job(任务)将会被**并行的**执行。



###### only and except
**only**和**except**两个参数说明了job什么时候将会被创建:

1.  **only**定义了job需要执行的所在分支或者标签
2.  **except**定义了job不会执行的所在分支或者标签

###### tags
**tags**这个参数是用来选择允许哪些runners来执行该jub的。

当你初始化Runner并注册一个Runner的时候，你被要求为Runner指定一个或多个标签，例如我的一个Runner被注册为**test1**。

job:
    tags:
        - test1
        - ruby

上面的声明将会保证该job将会被标签上有**test1**和**ruby**的runner所执行。如果没有就不执行


###### when
**when**参数是确定该job在失败或者没失败的时候执行不执行的参数。
**when**支持以下几个值之一:
1.  **on_success** 只有在之前场景执行的所有作业成功的时候才执行当前job，这个就是默认值，我们用最小配置的时候他默认就是这个值，所以失败的时候pipeline会停止执行后续任务
2.  **on_failure** 只有在之前场景执行的任务中至少有一个失败的时候才执行
3.  **always** 不管之前场景阶段的状态，总是执行
4.  **manual** ~手动执行job的时候触发（webui上点的）。请阅读[manual action](https://link.segmentfault.com/?enc=lgNdOTu10HFniMWqAxhEtg%3D%3D.ONXGY0piL893u%2FkS0i5i1Ur4Q8mzDWFXWumNZUAPvTKZzi5bcIWUXLutvnVeT9tHEVwyhU7aCTuI5l9OFUmkEw%3D%3D)

下面是例子:
```stages:
- build
- cleanup_build
- test
- deploy
- cleanup

build_job:
  stage: build
  script:
  - make build

cleanup_build_job:
  stage: cleanup_build
  script:
  - cleanup build when failed
  when: on_failure

test_job:
  stage: test
  script:
  - make test

deploy_job:
  stage: deploy
  script:
  - make deploy
  when: manual

cleanup_job:
  stage: cleanup
  script:
  - cleanup after jobs
  when: always
  ```

上面的例子将会:

1.  只有在 **build_job**失败的时候执行**cleanup_build_job**
2.  在pipeline最后一步，不管前面是失败或者成功，执行**cleanup_job**
3.  允许你在GitLabUI上手动执行deploy_job



#### 部署镜像
部署需要登录远程服务器，则需要远程免密登录。需要配置令牌。
1. 通过本地gitlab服务器，切换gitlab-runner账户。生成对应ssh秘钥
2. 使用 `ssh-copy-id  uname@ip` 命名配置令牌




遇到的问题及解决方法
1. gitlab-runner 使用shell登录远程服务器时。免密登录失败，提示 ` Host key verification failed.`
	gitlab-runner 会创建一个gitlab-runner的账户。gitlab-runner使用shell时会使用通过本地的gitlab-runner账户进行脚本操作。所以免密登录的配置需要在gitlab-runner账户下配置
	![[Pasted image 20220401163804.png]]
使用`ssh-copy-id uname@ip`  进行服务器免密登录配置