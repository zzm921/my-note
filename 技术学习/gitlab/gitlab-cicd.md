## Gitlab CI/CD 介绍

Gitlab CI/CD 是一款用于持续集成（CI），持续交付（CD）的工具，相似的工具有Jenkins、Travis CI、GoCD等。

持续集成，即Continuous Integration， 即在源代码变更后（git push）后自动检测（code lint）、构建和进行单元测试的过程，持续集成的目标是快速确保开发人员新提交的代码是好的（少bug），并且适合在代码库中进一步使用。

持续交付，即Continuous Delivery， 通常是指整个流程链（管道），它自动监测源代码变更并通过构建、测试、打包和相关操作运行它们以生成可部署的版本（可以是apk打包，也可以是网站部署），基本上没有任何人为干预。它包括持续集成，持续测试（保证代码质量），持续部署（自动发布版本，供用户使用）。

Gitlab的CI/CD算是比较简单的了，只需要依靠一份".gitlab-ci.yml"，将该文件随代码上传，Gitlab就会自动执行相应的任务，从而实现CI/CD。


## Gitlab-ci编写

`.gitlab-ci.yml`遵循YAML文件的语法，这份文件记录了你想要执行的各种指令，这些指令可以用来对你的代码进行规范检查（例如PEP8）、自动打包（例如Android自动打包）、自动部署等。

对于新手，如果不知道自己写的`.gitlab-ci.yml`是否有错误，可以通过Gitlab自带的`CI Lint`进行检查。

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

### image

该关键字指定一个任务（job）所使用的docker镜像，例如`image: python:latest`使用Python的最新镜像。

镜像下载的策略：

-   never： 当使用这个策略，会禁止Gitlab Runner从Docker hub或者其他地方下拉镜像，只能使用自己手动下拉的镜像
-   if-not-present： 当使用这个策略，Runner会先检测本地是否有镜像，有的话使用该镜像，如果没有再去下拉。这个策略如果再配合定期删除镜像，就能达到比较好的效果。
-   always： 这个是gitlab-ci默认使用的策略，即每一次都是重新下拉镜像，导致的结果就是比较耗时间


### services

该关键字指向其他Docker镜像，这些镜像会与image关键字指定的镜像绑定（link）。比如可以绑定一个mysql服务，存储单元测试所需要的假数据。

```
default_job:
  image: python:3.6

  services:
    - mysql:5.7

  before_script:
    - apt-get install mysql-client
```

### before_script和after_script

before_script关键字定义了一组在每个任务开始之前需要执行的命令，after_script则相反。例如可以在before_script做好ssh连接的准备，见下文。

注：before_script可以针对全部任务，也可以针对单个任务。

### stages

前面提到，我们可以定义一系列任务（job）去执行我们想要的指令，但怎样指定先后顺序呢，这就需要用到stages关键字了。

stages关键字有两个特性：  
1.如果两个任务对应的stage名相同，则这两个任务会并行运行  
2.下一个stage关联的任务会等待上一个stage执行成功后才继续运行，失败则不运行

```
image: python:3.6

stages:
  - build
  - test
  - deploy
# build-job1和build-job2会并行执行
build-job1:
  stage: build
  script:
    - echo $PWD

build-job2:
  stage: build
  script:
    - echo $PWD

# 这个任务会在build-job1和build-job2执行成功后再运行
test-job:
  stage: test
  script:
    - echo $PWD

# 注意定义的stage都需要用到
deploy-job:
  stage: deploy
  script:
    - echo $PWD

```

效果图如下：

![](https://p1-jj.byteimg.com/tos-cn-i-t2oaga2asx/gold-user-assets/2020/1/11/16f9335d6e468db4~tplv-t2oaga2asx-zoom-in-crop-mark:3024:0:0:0.awebp)

注：如果想要控制某一个stage在最开始，或者最后执行，可以使用`.pre` 和 `.post` 关键字

### only / except

这两个是让我又爱有恨的字段， 没有之一。

为了更好地说明，我们还需引入一个`Pipelines`的概念，Pipelines就是我们在Gitlab的UI界面看到一行行记录：

![](https://p1-jj.byteimg.com/tos-cn-i-t2oaga2asx/gold-user-assets/2020/1/11/16f93362bb607d1c~tplv-t2oaga2asx-zoom-in-crop-mark:3024:0:0:0.awebp)

如上图，一共有三个Pipelines，每个Pipelines内部就是我们定义的任务的执行情况，就是这么简单。

前面提到，通过stages关键字可以控制任务执行的先后顺序，而通过`only/except`关键字控制的是任务的触发条件。

only/except关键字包含了一些子关键字（或者你可以理解为策略），当符合定义的策略时才会触发Pipelines的执行，except则相反。

only关键字的默认策略是['branches', 'tags']，即你提交了一个分支或者打了标签，就会触发，

除此之外，only/except关键字还有基础特性和高级特性之分，所包含的子关键字也各不相同，建议还是仔细阅读官方文档。

only/except(basic)：

-   branches: 当你的Git Refs对应的是一个分支时触发
-   tags: 当你的Git Refs对应的是一个标签时触发
-   pushes: 当你使用`git push`时触发
-   web: 当你使用Web界面的`Run Pipeline`时触发
-   merge_requests: 当你创建或者更新一个merge_requests时触发
-   ...



下面是一些示例，希望能给你带来帮助

1.当提交的分支为master才会触发Pipelines

```
image: python:3.6

# 第一种方式
job1:
  only:
    - master
  script:
    - echo $PWD

# 第二种方式
job2:
  only:
    refs:
      - master
  script:
    - echo $PWD

# 第三种方式
job3:
  only:
    variables:
      - $CI_COMMIT_REF_NAME == "master"
  script:
    - echo $PWD
```

2.当打了tag才会触发Pipelines（正常的提交不会）

```
image: python:3.6

# 第一种方式
job1:
  only:
    - tags
  script:
    - echo $PWD
  
# 第二种方式
job2:
  only:
    refs:
      - tags
  script:
    - echo $PWD
```

3.当提交的分支为master或者打了tags触发Pipelines

```
image: python:3.6

# 举这个例子是想说明only关键字之间的关系是”或“关系
job1:
  only:
    - master
    - tags
  script:
    - echo $PWD
```

4.当提交的分支为master且打了tags触发Pipelines  
目前没找到办法，应该可以配合`rules`关键字实现

5.当使用Web界面的`Run Pipelines`时触发（个人感觉这种方式挺有用的）

```
image: python:3.6

# 举这个例子是想说明only关键字之间的关系是”或“关系
job1:
  only:
    - web
  script:
    - echo $PWD
```


### tags

该关键字指定了使用哪个Runner（哪个机器）去执行我们的任务，注意与上文only关键字的tags进行区分。

```
image: python:3.6

# 举这个例子是想说明only关键字之间的关系是”或“关系
job1:
  only:
    - dev
  tags:
    - machine1
  script:
    - echo $PWD
```

### when

前面说过，stages关键字可以控制每个任务的执行顺序，且后一个stage会等待前一个stage执行成功后才会执行，那如果我们想要达到前一个stage失败了，后面的stage仍然能够执行的效果呢？

这时候when关键字就可以发挥作用了，它一共有五个值：

-   on_success：只有前面stages的所有工作成功时才执行，这是默认值。
-   on_failure：当前面stages中任意一个jobs失败后执行
-   always：无论前面stages中jobs状态如何都执行
-   manual：手动执行
-   delayed：延迟执行

```
# 官方示例
stages:
  - build
  - cleanup_build
  - test
  - deploy
  - cleanup

build_job:
  stage: build
  script:
    - make build

# 如果build_job任务失败，则会触发该任务执行
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

# 总是执行
cleanup_job:
  stage: cleanup
  script:
    - cleanup after jobs
  when: always
```

### 变量

Gitlab-CI的变量有几种，分别为预先定义的环境变量，比如`CI_COMMIT_SHA`, `CI_COMMIT_MESSAGE`; 通过Web界面Settings/CI-CD设置的变量，以及自己在`.gitlab-ci.yml`定义的变量。

通过预先定义的环境变量，我们可以获取分支名，提交的消息，从而判断任务是否需要执行；而Web界面Settings/CI-CD设置的变量，则非常适合用于存储像公私钥，账号密码这些不便公开的数据。因为只有Owner和Maintainer能够查看。

如下图就定义了一个`SSH_PRIVATE_KEY`来存储私钥：

![](https://p1-jj.byteimg.com/tos-cn-i-t2oaga2asx/gold-user-assets/2020/1/11/16f9336c06721134~tplv-t2oaga2asx-zoom-in-crop-mark:3024:0:0:0.awebp)

  
 