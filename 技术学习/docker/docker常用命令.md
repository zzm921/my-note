#### 删除所有none镜像
docker rmi $(docker images | grep "none" | awk '{print $3}')