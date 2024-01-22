### 现象
进程卡死，cpu占满。怀疑某个操作执行时间太长导致进程堵塞。cpu占满。后续请求无响应
### 分析 
alinode性能平台，早期已适配平台
1、查看后台是否有core Dump文件生成。查看无信息。由于保存了node进程状态。可手动生成coredump文件
2、生成coredump，使用gdb直接调试进程，生成core文件
https://zhuanlan.zhihu.com/p/74897601








```
gdb  hello  11111
gcore  //生成core文件
```
3、进入alinode性能平台可看到刚生成的core文件。进行转储和分析，可查看当前正在执行的函数及当前持有对象信息。排查分析问题

