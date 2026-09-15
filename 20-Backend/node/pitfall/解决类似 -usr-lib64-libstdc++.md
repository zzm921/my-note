解决类似 /usr/lib64/libstdc++.so.6: version `GLIBCXX_3.4.21' not found 的问题


源码编译升级安装了 gcc 后，编译程序或运行其它程序时，有时会出现类似 /usr/lib64/libstdc++.so.6: version `GLIBCXX_3.4.21' not found 的问题。这是因为升级 gcc 时，生成的动态库没有替换老版本 gcc 的动态库导致的，将 gcc 最新版本的动态库替换系统中老版本的动态库即可解决。


解决办法，更新gcc库
```
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install gcc-4.9
sudo apt-get upgrade libstdc++6
```


1. 问题原因分析

为了安装最新版本的 Node.js （最新版本的 Node.js 使用了 C++ 11 中，而 C++ 11 需要code>gcc 4.8+才能支持），将 gcc 升级到了当前最新版本 v 5.2.0 。升级后，成功编译安装了新版本的 Node.js （ v 4.2.1 ）,但运行时程序时出现了以下错误：
node: /usr/lib64/libstdc++.so.6: version `GLIBCXX_3.4.21' not found (required by node)
node: /usr/lib64/libstdc++.so.6: version `GLIBCXX_3.4.15' not found (required by node)
node: /usr/lib64/libstdc++.so.6: version `GLIBCXX_3.4.20' not found (required by node)

运行以下命令检查动态库：
strings /usr/lib64/libstdc++.so.6 | grep GLIBC




输出结果如下：
GLIBCXX_3.4
GLIBCXX_3.4.1
GLIBCXX_3.4.2
GLIBCXX_3.4.3
GLIBCXX_3.4.4
GLIBCXX_3.4.5
GLIBCXX_3.4.6
GLIBCXX_3.4.7
GLIBCXX_3.4.8
GLIBCXX_3.4.9
GLIBCXX_3.4.10
GLIBCXX_3.4.11
GLIBCXX_3.4.12
GLIBCXX_3.4.13
GLIBCXX_FORCE_NEW
GLIBCXX_DEBUG_MESSAGE_LENGTH

从以上输出可以看出， gcc 的动态库还是旧版本的。说明出现这些问题，是因为升级 gcc 时，生成的动态库没有替换老版本 gcc 的动态库。


2. 问题处理


最简单方法

下载一个  
libstdc++.so.6.0.21 的库 拷贝进电脑 ，就不需要升级gcc那么麻烦了

执行以下命令，查找编译 gcc 时生成的最新动态库：
find / -name "libstdc++.so*"

输出如下：
/home/gcc-5.2.0/gcc-temp/stage1-x86_64-unknown-linux-gnu/libstdc++-v3/src/.libs/libstdc++.so
/home/gcc-5.2.0/gcc-temp/stage1-x86_64-unknown-linux-gnu/libstdc++-v3/src/.libs/libstdc++.so.6
/home/gcc-5.2.0/gcc-temp/stage1-x86_64-unknown-linux-gnu/libstdc++-v3/src/.libs/libstdc++.so.6.0.21  //最新动态库
……


/home/gcc-5.2.0/gcc-temp 是 升级gcc 时的输出目录。

将上面的最新动态库 libstdc++.so.6.0.21 复制到 /usr/lib64 目录下：
cp /home/gcc-5.2.0/gcc-temp/stage1-x86_64-unknown-linux-gnu/libstdc++-v3/src/.libs/libstdc++.so.6.0.21 /usr/lib64




复制后，修改系统默认动态库的指向，即：重建默认库的软连接。

切换工作目录至 /usr/lib64 ：
cd /usr/lib64

删除原来软连接：
rm -rf libstdc++.so.6

将默认库的软连接指向最新动态库：
ln -s libstdc++.so.6.0.21 libstdc++.so.6




默认动态库升级完成。重新运行以下命令检查动态库：
strings /usr/lib64/libstdc++.so.6 | grep GLIBC

现在输出如下：
GLIBCXX_3.4
GLIBCXX_3.4.1
GLIBCXX_3.4.2
GLIBCXX_3.4.3
GLIBCXX_3.4.4
GLIBCXX_3.4.5
GLIBCXX_3.4.6
GLIBCXX_3.4.7
GLIBCXX_3.4.8
GLIBCXX_3.4.9
GLIBCXX_3.4.10
GLIBCXX_3.4.11
GLIBCXX_3.4.12
GLIBCXX_3.4.13
GLIBCXX_3.4.14
GLIBCXX_3.4.15
GLIBCXX_3.4.16
GLIBCXX_3.4.17
GLIBCXX_3.4.18
GLIBCXX_3.4.19
GLIBCXX_3.4.20
GLIBCXX_3.4.21
GLIBC_2.3
GLIBC_2.2.5
GLIBC_2.3.2
GLIBCXX_FORCE_NEW
GLIBCXX_DEBUG_MESSAGE_LENGTH


来源： 
https://itbilu.com/linux/management/NymXRUieg.html











升级 gcc


# 下载gcc 
5.2
.0
源码
wget http
:
/
/
ftp
.
gnu
.
org
/
gnu
/
gcc
/
gcc
-
5.2
.0
/
gcc
-
5.2
.0
.
tar
.
bz2
# 源码解压
tar xvf gcc
-5
.2
.0
.
tar
.
bz2 
cd gcc
-
5.2
.0

#下载一些必备的依赖程序

.
/
contrib
/
download_prerequisites
mkdir build 
&&
 cd build

.
.
/
configure 
--
enable
-
checking
=
release 
--
enable
-
languages
=
c
,
c
++
 
--
disable
-
multilib
# 开始编译，单线程编译要花费很长时间，
# 可以考虑用
-
j参数执行并行编译如： make 
-
j8， 
8
是指
8
个线程并行，
# 但如果并行编译过程出错，有时很难发现
make
# 安装
,
需要root权限
sudo make install


来源： 
https://cloud.tencent.com/developer/article/1433688