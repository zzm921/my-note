升级须知
升级须知
gitlab跨大版本容易出错，需按照官方版本一步一步进行升级，升级前做好数据备份


### 方案介绍
公司原版本为源码安装gitlab6.9，由于源码安装升级麻烦，先将版本迁移到rpm版本，再由rpm版本进行升级。
升级路径为
6.9.2-> 7.10.4->8.2->8.11.0 -> 8.12.0 -> 8.17.7 -> 9.5.10 -> 10.8.7 -> 11.11.8 -> 12.0.12 -> 12.1.17 -> 12.10.14 -> 13.0.14 -> 13.1.11 -> 13.8.8 -> 13.12.15 -> 14.0.12 -> 14.9.0
路径参考
https://doc.devpod.cn/gitlab/gitlab-4980764.html#GitLab%E7%89%88%E6%9C%AC%E5%8D%87%E7%BA%A7%E8%B7%AF%E5%BE%84-GitLab%E5%8D%87%E7%BA%A7%E8%B7%AF%E5%BE%84%E7%A4%BA%E4%BE%8B

由于ubuntu14 只支持到 gitlab11.10.8，所以此次升级路线为
6.9.2-> 7.10.4->8.2->8.11.0 -> 8.12.0 -> 8.17.7 -> 9.5.10 -> 10.8.7 -> 11.10.8


测试时发现 gitlab11需要的postgresql需要9.6




### 数据备份
安装包
gitlab-rake gitlab:backup:create
源码安装
sudo -u git -H bundle exec rake gitlab:backup:create RAILS_ENV=production
docker安装
docker exec -t gitlab-rake gitlab:backup:create

### 从源码转为rpm安装
#### 安装包安装gitlab6.9.2

参考
https://blog.securityevaluators.com/upgrading-gitlab-ce-from-a-6-9-2-source-installation-to-10-1-0-omnibus-a-novel-cf8c4f78bf99


#### 前期准备
脚本  
我们的机器安装了多个版本的 PostgreSQL，所以为了让 GitLab 满意，我必须做一些符号链接，`/usr/bin/pg_dump`并`/usr/bin/psql`指向适当的版本
```
mv /opt/gitlab/embedded/bin/psql /opt/gitlab/embedded/bin/psql.bak

mv /opt/gitlab/embedded/bin/pg_dump /opt/gitlab/embedded/bin/pg_dump.bak

ln -s /usr/bin/psql /opt/gitlab/embedded/bin/psql

ln -s /usr/bin/pg_dump /opt/gitlab/embedded/bin/pg_dump
```

#### 备份gitlab数据
```
cd /home/git/gitlab

sudo -u git -H bundle exec rake gitlab:backup:create RAILS_ENV=production

//生成文件
/home/git/gitlab/tmp/backups/1653532072_gitlab_backup.tar


```

这应该在目录中创建一个备份文件`/home/git/gitlab/tmp/backups/`


#### rpm安装gitlab6.9
###### 创建gitlab配置文件 `gitlab.rb`
```
external_url ' [http://not.the.actual.url']

# 数据库配置 使用已有数据库
postgresql['enable'] = false  
gitlab_rails['db_host'] = '/var/run/postgresql'  
gitlab_rails['db_port'] = '5432'  
gitlab_rails[' db_username'] = 'git'

# 邮箱配置

gitlab_rails['smtp_enable'] = true
gitlab_rails['smtp_address'] = "smtp.exmail.qq.com"
gitlab_rails['smtp_port'] = 465
gitlab_rails['smtp_user_name'] = "zhangzheming@cocheer.net"
gitlab_rails['smtp_password'] = "824781943Asa"
gitlab_rails['smtp_domain'] = "zhangzheming@cocheer.net"
gitlab_rails['smtp_authentication'] = "login"
gitlab_rails['smtp_enable_starttls_auto'] = true
gitlab_rails['smtp_tls'] = false
gitlab_rails['smtp_pool'] = false

```

###### 安装

```


dpkg -i /home/wmclaughlin/GITLAB-UPGRADE/packages/gitlab_6.9.2-omnibus.2-1_amd64.deb

mkdir -p /etc/gitlab

cp ./gitlab.rb /etc/gitlab/gitlab.rb

service gitlab stop

gitlab-ctl reconfigure


gitlab-ctl restart

gitlab-ctl stop unicorn

gitlab-ctl stop sidekiq

gitlab-ctl status

//复制备份文件到新gitlab
cp /home/git/gitlab/tmp/backups/1653532072_gitlab_backup.tar /var/opt/gitlab/backups/


gitlab-rake gitlab:backup:restore BACKUP=1653532072


//设置权限

sudo chmod -R ug+rwX,o-rwx /var/opt/gitlab/git-data/repositories
sudo chmod -R ug-s /var/opt/gitlab/git-data/repositories


// 检测是否正常
gitlab-rake gitlab:check SANITIZE=true

```


#### 升级到 7.10.4

```
dpkg -i ./gitlab-ce_7.10.4~omnibus-1_amd64.deb

# ## Installing pg_trgm

apt-get install -y postgresql-contrib-9.3

gitlab-ctl restart

# 切换账号
su - postgres
psql -p 5432 -s gitlabhq_production

CREATE EXTENSION pg_trgm;

## Repairing PostgreSQL symlinks
./fix_psql_links.sh



```

#### 升级到 8.10.0
```
wget --content-disposition https://packages.gitlab.com/gitlab/gitlab-ce/packages/ubuntu/trusty/gitlab-ce_8.10.0-ce.1_amd64.deb/download.deb

sudo dpkg -i gitlab-ce_8.10.0-ce.1_amd64.deb

## 将postgresql改为内置的
修改 /etc/gitlab/gitlab.rb文件

postgresql[‘enable’]=true



gitlab-ctl reconfigure

sh ./fix_psql_links.sh

```

#### 升级到 8.11.0
```
wget --content-disposition https://packages.gitlab.com/gitlab/gitlab-ce/packages/ubuntu/trusty/gitlab-ce_8.11.0-ce.1_amd64.deb/download.deb

sudo dpkg -i ./gitlab-ce_8.11.0-ce.0_amd64.deb

sudo gitlab-ctl reconfigure

sudo gitlab-ctl restart 


# 查看仓库
gitlab-rake gitlab:check SANITIZE=true

#确保没问题重设权限

sudo chown -R git /var/opt/gitlab/gitlab-rails/uploads
sudo find /var/opt/gitlab/gitlab-rails/uploads -type f -exec chmod 0644 {} \;
sudo find /var/opt/gitlab/gitlab-rails/uploads -type d -not -path /var/opt/gitlab/gitlab-rails/uploads -exec chmod 0700 {} \;

sudo ./fix_psql_links.sh

```

#### 升级到  `8.17.7`
```
wget --content-disposition https://packages.gitlab.com/gitlab/gitlab-ce/packages/ubuntu/trusty/gitlab-ce_8.17.7-ce.0_amd64.deb/download.deb


sudo dpkg -i ./gitlab-ce_8.17.7-ce.0_amd64.deb


sudo gitlab-ctl reconfigure
sudo gitlab-ctl restart 




```


#### 升级到  9.5.10
```
wget --content-disposition https://packages.gitlab.com/gitlab/gitlab-ce/packages/ubuntu/trusty/gitlab-ce_9.5.10-ce.0_amd64.deb/download.deb


sudo dpkg -i ./gitlab-ce_9.5.10-ce.0_amd64.deb


sudo gitlab-ctl reconfigure
sudo gitlab-ctl restart 


```

#### 升级到10.8.7
```
wget --content-disposition https://packages.gitlab.com/gitlab/gitlab-ce/packages/ubuntu/trusty/gitlab-ce_9.5.10-ce.0_amd64.deb/download.deb


sudo dpkg -i ./gitlab-ce_9.5.10-ce.0_amd64.deb


sudo gitlab-ctl reconfigure
sudo gitlab-ctl restart 


```


#### 升级到11.10.8
```
wget --content-disposition https://packages.gitlab.com/gitlab/gitlab-ce/packages/ubuntu/trusty/gitlab-ce_11.10.8-ce.0_amd64.deb/download.deb


sudo dpkg -i ./gitlab-ce_11.10.8-ce.0_amd64.deb


sudo gitlab-ctl reconfigure
sudo gitlab-ctl restart 

```

