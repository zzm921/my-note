1、启动飞牛ssh功能，并登录ssh
sudo cp /etc/fstab /etc/fstab.old
sudo vi /etc/fstab
添加


//192.168.2.130/照片 /vol1/1000/Photos/smbPic cifs username=ASUS,password=zhexia,iocharset=utf8,gid=1000,uid=1000,file_mode=0777,dir_mode=0777 0 0


sudo mount -a

参考