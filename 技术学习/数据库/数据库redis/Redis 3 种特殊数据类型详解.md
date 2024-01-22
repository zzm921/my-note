除了5种基本数据类型之外，redis嗐支持3种特殊的数据类型：Bitmap、HyperLogLog、GEO。
### Bitmap（位图）
Bitmap存储的是连续的二进制数字，通过Bitmap，只需要一个bit位来表示某个元素对应的值或者状态，key就是对应元素本身。我们知道8个bit可以组成一个byte，所以Bitmap本身会极大的界山存储空间。
你可以将Bitmap看做一个存储二进制数据的数组，数组中每个元素的下标叫做offset。
### 常用命令

|命令|介绍|
|---|---|
|SETBIT key offset value|设置指定 offset 位置的值|
|GETBIT key offset|获取指定 offset 位置的值|
|BITCOUNT key start end|获取 start 和 end 之前值为 1 的元素个数|
|BITOP operation destkey key1 key2 ...|对一个或多个 Bitmap 进行运算，可用运算符有 AND, OR, XOR 以及 NOT|

#### 应用场景
需要保存状态信息(0/1即可表示)的场景。如：用户签到情况、活跃用户情况、用户行为统计。

### HyperLogLog(基数统计)
HyperLogLog 是一种有名的基数计数概率算法，基于LogLog Counting优化改进的来，并不是redis特有的，redis只是实现了这个算法并提供一些开箱即用的
####  常用命令
HyperLogLog 相关的命令非常少，最常用的也就 3 个。

|命令|介绍|
|---|---|
|PFADD key element1 element2 ...|添加一个或多个元素到 HyperLogLog 中|
|PFCOUNT key1 key2|获取一个或者多个 HyperLogLog 的唯一计数。|
|PFMERGE destkey sourcekey1 sourcekey2 ...|将多个 HyperLogLog 合并到 destkey 中，destkey 会结合多个源，算出对应的唯一计数。|

### Geospatial(地理位置)
Geospatial index（地理空间索引，简称GEO）主要用于存储地理位置信息，基于sorted set实现。
通过GEO我们可以轻松事项两个位置距离的计算，获取指定位置附近元素等功能。
#### 常用命令

|命令|介绍|
|---|---|
|GEOADD key longitude1 latitude1 member1 ...|添加一个或多个元素对应的经纬度信息到 GEO 中|
|GEOPOS key member1 member2 ...|返回给定元素的经纬度信息|
|GEODIST key member1 member2 M/KM/FT/MI|返回两个给定元素之间的距离|
|GEORADIUS key longitude latitude radius distance|获取指定位置附近 distance 范围内的其他元素，支持 ASC(由近到远)、DESC（由远到近）、Count(数量) 等参数|
|GEORADIUSBYMEMBER key member radius distance|类似于 GEORADIUS 命令，只是参照的中心点是 GEO 中的元素|

---

著作权归JavaGuide(javaguide.cn)所有 基于MIT协议 原文链接：https://javaguide.cn/database/redis/redis-data-structures-02.html