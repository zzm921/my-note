---
type: howto
domain: ops/docker
tags: [docker]
status: draft
updated: 2026-09-16
---

#### 删除所有none镜像
docker rmi $(docker images | grep "none" | awk '{print $3}')