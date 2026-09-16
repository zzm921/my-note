---
type: concept
domain: ops/vm
tags: [CentOS, 虚拟机, 运维]
status: draft
updated: 2026-09-16
---

centos虚拟机问题
1、安装完成后无网络问题
修改网卡配置
```
vi /etc/sysconfig/network-scripts/ifcfg-ens33

ONBOOT=no，改为ONBOOT=yes


增加
DNS1=8.8.8.8



重启网络
systemctl restart network

```




centos 开启端口
https://codeantenna.com/a/gdutDTE2Tj

