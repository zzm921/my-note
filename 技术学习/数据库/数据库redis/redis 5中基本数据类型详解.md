redis共有5种基本数据类型：string，list，set，hash，zset（有序集合）
这五种数据类型是直接给用户使用的，是数据的保存形式，其底层实现主要依赖这8中数据结构：简单动态字符串（sds）、LinkedList（双向链表）、Dict（哈希表/词典）、SkipList（跳跃表）、Intest（整数集合）、ZipList（压缩列表）、QuickList（快速列表）
Redis 5 种基本数据类型对应的底层数据结构实现如下表所示：

|String|List|Hash|Set|Zset|
|---|---|---|---|---|
|SDS|LinkedList/ZipList/QuickList|Dict、ZipList|Dict、Intset|ZipList、SkipList|

Redis 3.2 之前，List 底层实现是 LinkedList 或者 ZipList。 Redis 3.2 之后，引入了 LinkedList 和 ZipList 的结合 QuickList，List 的底层实现变为 QuickList。从 Redis 7.0 开始， ZipList 被 ListPack 取代。

### string（字符串）
string是redis中最简单同事也是最常用的一个数据类型。
string是一种二进制安全的数据类型，可以用来存储任何类型的数据，比如字符串、整数、浮点数、图片、序列化后的对象。
虽然 Redis 是用 C 语言写的，但是 Redis 并没有使用 C 的字符串表示，而是自己构建了一种 **简单动态字符串**（Simple Dynamic String，**SDS**）。相比于 C 的原生字符串，Redis 的 SDS 不光可以保存文本数据还可以保存二进制数据，并且获取字符串长度复杂度为 O(1)（C 字符串为 O(N)）,除此之外，Redis 的 SDS API 是安全的，不会造成缓冲区溢出。
### 常用命令

|命令|介绍|
|---|---|
|SET key value|设置指定 key 的值|
|SETNX key value|只有在 key 不存在时设置 key 的值|
|GET key|获取指定 key 的值|
|MSET key1 value1 key2 value2 ……|设置一个或多个指定 key 的值|
|MGET key1 key2 ...|获取一个或多个指定 key 的值|
|STRLEN key|返回 key 所储存的字符串值的长度|
|INCR key|将 key 中储存的数字值增一|
|DECR key|将 key 中储存的数字值减一|
|EXISTS key|判断指定 key 是否存在|
|DEL key（通用）|删除指定的 key|
|EXPIRE key seconds（通用）|给指定 key 设置过期时间|
####  应用场景
**需要存储常规数据的场景**
- 举例：缓存 Session、Token、图片地址、序列化后的对象(相比较于 Hash 存储更节省内存)。
- 相关命令：`SET`、`GET`。
**需要计数的场景**
- 举例：用户单位时间的请求数（简单限流可以用到）、页面单位时间的访问数。
- 相关命令：`SET`、`GET`、 `INCR`、`DECR` 。
**分布式锁**
利用 `SETNX key value` 命令可以实现一个最简易的分布式锁（存在一些缺陷，通常不建议这样实现分布式锁）。

### List（列表）
redis中的list其实就是链表数据结构的实现。redis的list的实现为一个双向链表，既可以支持反向查找和表里，更方便操作，不过带来了部分额外的内存开销。
![[Pasted image 20231205170612.png]]
#### 常用命令

|命令|介绍|
|---|---|
|RPUSH key value1 value2 ...|在指定列表的尾部（右边）添加一个或多个元素|
|LPUSH key value1 value2 ...|在指定列表的头部（左边）添加一个或多个元素|
|LSET key index value|将指定列表索引 index 位置的值设置为 value|
|LPOP key|移除并获取指定列表的第一个元素(最左边)|
|RPOP key|移除并获取指定列表的最后一个元素(最右边)|
|LLEN key|获取列表元素数量|
|LRANGE key start end|获取列表 start 和 end 之间 的元素|

### Hash（哈希）
redis中的hash是一个string类型的field-value的映射表，特别适合用于存储对象，后续操作的时候你可以直接修改这个对象中的某些字段的值。
#### 常用命令

|命令|介绍|
|---|---|
|HSET key field value|设置指定哈希表中指定字段的值|
|HSETNX key field value|只有指定字段不存在时设置指定字段的值|
|HMSET key field1 value1 field2 value2 ...|同时将一个或多个 field-value (域-值)对设置到指定哈希表中|
|HGET key field|获取指定哈希表中指定字段的值|
|HMGET key field1 field2 ...|获取指定哈希表中一个或者多个指定字段的值|
|HGETALL key|获取指定哈希表中所有的键值对|
|HEXISTS key field|查看指定哈希表中指定的字段是否存在|
|HDEL key field1 field2 ...|删除一个或多个哈希表字段|
|HLEN key|获取指定哈希表中字段的数量|
|HINCRBY key field increment|对指定哈希中的指定字段做运算操作（正数为加，负数为减）|

### Set（集合）
redis中的Set类型是一种无须集合，集合中的元素没有先后循序但都唯一。当你需要存储一个列表的数据，又不希望出现重复数据是，set是一个很好的选择，并且Set提供了判断某个元素是否在set集合内的重要接口，这个也是List说不能提供的。
#### 常用命令

|命令|介绍|
|---|---|
|SADD key member1 member2 ...|向指定集合添加一个或多个元素|
|SMEMBERS key|获取指定集合中的所有元素|
|SCARD key|获取指定集合的元素数量|
|SISMEMBER key member|判断指定元素是否在指定集合中|
|SINTER key1 key2 ...|获取给定所有集合的交集|
|SINTERSTORE destination key1 key2 ...|将给定所有集合的交集存储在 destination 中|
|SUNION key1 key2 ...|获取给定所有集合的并集|
|SUNIONSTORE destination key1 key2 ...|将给定所有集合的并集存储在 destination 中|
|SDIFF key1 key2 ...|获取给定所有集合的差集|
|SDIFFSTORE destination key1 key2 ...|将给定所有集合的差集存储在 destination 中|
|SPOP key count|随机移除并获取指定集合中一个或多个元素|
|SRANDMEMBER key count|随机获取指定集合中指定数量的元素|


### sorted Set（有序集合）
sorted Set类似于set，但和set相比，sorted set增加了一个权重参数score，使得集合中的元素能够按score进行有序的排列，还可以通过score的范围来获取元素列表。有点像java中的hashmap和treeset的结合体。
![[Pasted image 20231206112913.png]]
#### 常用命令

|命令|介绍|
|---|---|
|ZADD key score1 member1 score2 member2 ...|向指定有序集合添加一个或多个元素|
|ZCARD KEY|获取指定有序集合的元素数量|
|ZSCORE key member|获取指定有序集合中指定元素的 score 值|
|ZINTERSTORE destination numkeys key1 key2 ...|将给定所有有序集合的交集存储在 destination 中，对相同元素对应的 score 值进行 SUM 聚合操作，numkeys 为集合数量|
|ZUNIONSTORE destination numkeys key1 key2 ...|求并集，其它和 ZINTERSTORE 类似|
|ZDIFFSTORE destination numkeys key1 key2 ...|求差集，其它和 ZINTERSTORE 类似|
|ZRANGE key start end|获取指定有序集合 start 和 end 之间的元素（score 从低到高）|
|ZREVRANGE key start end|获取指定有序集合 start 和 end 之间的元素（score 从高到底）|
|ZREVRANK key member|获取指定有序集合中指定元素的排名(score 从大到小排序)|
