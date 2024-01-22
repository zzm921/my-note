### 一、GitLab Runner 介绍

GitLab Runner是一个开源项目，用于运行您的作业并将结果发送回GitLab。它与GitLab CI一起使用，GitLab CI是GitLab随附的开源持续集成服务，用于协调作业。

GitLab Runner是用Go编写，可以作为单个二进制文件运行，不需要语言特定的要求。

### 二、GitLab Runner的三种类型

shared：运行整个平台项目的作业(gitlab)

group：运行特定group下的所有项目的作业(group)

specific：运行指定的项目作业(project)

### 三、GitLab Runner两种状态

locked：无法运行项目作业

paused：不会运行作业

### 四、GitLab Runner安装

由于目前服务都上容器了，因此这里只演示采用docker安装GitLab Runner的方法，其他的方法可参考官网。

官网地址：[https://docs.gitlab.com/runner/install/](https://link.zhihu.com/?target=https%3A//docs.gitlab.com/runner/install/)

```text
$ mkdir -p /data/gitlab-runner/config

$ docker run -itd --restart=always --name gitlab-runner \
-v /data/gitlab-runner/config:/etc/gitlab-runner \
-v /var/run/docker.sock:/var/run/docker.sock  gitlab/gitlab-runner:latest

$ docker exec -it gitlab-runner bash
root@24dc60abee0b:/# gitlab-runner -v
Version:      13.8.0
Git revision: 775dd39d
Git branch:   13-8-stable
GO version:   go1.13.8
Built:        2021-01-20T13:32:47+0000
OS/Arch:      linux/amd64
```

同样也可使用docker-compose跟gitlab一起安装

### 五、GitLab Runner注册

注意：注册gitlab-runner的前提是必须有一个可以使用的gitlab仓库

进入项目，点击【设置】-> 【CI/CD】-> 【runner】，可以看到界面右边有gitlab的地址和token。这个需要用于后面runner的注册使用。

由于runner是采用docker安装，因此注册的时候需要进入到runner的容器中进行

```text
[root@localhost config]# docker exec -it gitlab-runner bash

root@24dc60abee0b:/# gitlab-runner register
Runtime platform                                    arch=amd64 os=linux pid=86 revision=775dd39d version=13.8.0
Running in system-mode.                            
                                                   
Enter the GitLab instance URL (for example, https://gitlab.com/):
http://192.168.50.128/
Enter the registration token:
iqxKz5XTz4w_2RxiSQ5S
Enter a description for the runner:
[24dc60abee0b]: node1.ayunw.cn
Enter tags for the runner (comma-separated):
default
Registering runner... succeeded                     runner=iqxKz5XT
Enter an executor: docker-ssh+machine, kubernetes, custom, shell, ssh, virtualbox, docker, docker-ssh, parallels, docker+machine:
docker
Enter the default Docker image (for example, ruby:2.6):
docker:19.03.15
Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded! 

root@24dc60abee0b:/# gitlab-runner restart
Runtime platform                                    arch=amd64 os=linux pid=98 revision=775dd39d version=13.8.0
Terminated

root@24dc60abee0b:/# gitlab-runner list 
Runtime platform                                    arch=amd64 os=linux pid=130 revision=775dd39d version=13.8.0
Listing configured runners                          ConfigFile=/etc/gitlab-runner/config.toml
node1.ayunw.cn                                      Executor=docker Token=VSVWeipeMirJsJo9znT5 URL=http://192.168.50.128/
```

runner注册完成后会在 /etc/gitlab-runner目录下生成一个config.toml的文件。这个就是runner的配置文件。因为在安装runner的时候我们已经将配置文件的目录通过挂载的形式映射到了宿主机目录：/data/gitlab-runner/config 下，所以后续如果需要更新runner配置文件可以直接在宿主机上进行修改。并且在宿主机上进行修改runner配置文件不需要重启runner。它会每5分钟检查一次文件自动获取所有更改。包括该[[runners]]部分中定义的任何参数以及全局部分中的大多数参数（除外）listen_address。

配置如下：

```text
root@24dc60abee0b:/etc/gitlab-runner# cat config.toml 
concurrent = 1
check_interval = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "node1.ayunw.cn"
  url = "你的gitlab访问的url地址"
  token = "在gitlab的ui上看到的token"
  executor = "docker"
  [runners.custom_build_dir]
  [runners.cache]
    [runners.cache.s3]
    [runners.cache.gcs]
    [runners.cache.azure]
  [runners.docker]
    tls_verify = false
    image = "docker:19.03.15"
    privileged = false
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/cache"]
    shm_size = 0
```

注册完成后，返回gitlab的ui查看注册的runner。 

可以看到当前的runner是锁定的状态。如果需要使用这个runner，需要将它解锁。我们可以点击右边的编辑，然后将 "锁定到当前项目"取消勾选。再将运行未标记的作业勾选上。现在runner就可以运行了。

### 六、测试pipeline

新建一个项目，然后在项目根目录提交一个 .gitlab-ci.yml 的文件，内容如下。当提交了以后，这时候就会触发pipeline流水线了。

```text
stages:
  - maven
  - build
  - deploy
  
maven_job:
  stage: maven
  tags:
    - default
  only:
    - master
  script:
    - echo "This is the first maven job"
    
build_job:
  stage: build
  tags:
    - default
  only:
    - master
  script:
    -  echo "This is the first build job"

deploy_job:
  stage: deploy
  tags:
    - default
  only:
    - master
  script:
    - echo "This is the first deploy job"
```

至此，gitlab runner安装完成且整个pipeline流水线可以正常运行。