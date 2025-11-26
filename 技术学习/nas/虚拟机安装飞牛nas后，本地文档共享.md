### 通过smb挂载
1、启动飞牛ssh功能，并登录ssh
sudo cp /etc/fstab /etc/fstab.old
sudo vi /etc/fstab
添加


//192.168.2.130/照片 /vol1/1000/Photos/smbPic cifs username=ASUS,password=zhexia,iocharset=utf8,gid=1000,uid=1000,file_mode=0777,dir_mode=0777 0 0


sudo mount -a

参考 https://zhuanlan.zhihu.com/p/21249841926



### 通过虚拟机共享文件夹
1、vm添加共享文件夹  设置-共享文件夹

2、ssh登录
sudo apt-get update
sudo apt-get install open-vm-tools open-vm-tools-desktop -y

3、配置文件夹
手动
sudo vmhgfs-fuse .host:/ /vol1/1000/vm -o allow_other

自动配置
sudo vi /etc/fstab
host:/ /vol1/1000/vm fuse.vmhgfs-fuse allow_other,defaults 0 0
