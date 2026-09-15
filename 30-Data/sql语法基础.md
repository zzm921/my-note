### 基本概念
#### 数据库术语
- 数据库：保存有组织的数据的容器
- 数据表：某种特定类型数据的结构化清单
- 模式：关于数据库的表和分布及特性信息。模式定义了数据在表中如何存储，包含存储什么样的数据，数据如何分解，各部分信息如何命名等信息。数据库和表都有模式
- 列：表中的一个字段。所有表都是有一个或者多个列组成的。
- 行：表中的一个记录
- 主键：一列能唯一标识表中的每一行。
#### sql分类
#### 数据定义语言（DDL）

数据定义语言（Data Definition Language，DDL）是 SQL 语言集中负责数据结构定义与数据库对象定义的语言。
DDL 的主要功能是**定义数据库对象**。
DDL 的核心指令是 `CREATE`、`ALTER`、`DROP`。

数据操纵语言（DML）
数据操纵语言（Data Manipulation Language, DML）是用于数据库操作，对数据库其中的对象和数据运行访问工作的编程语句。
DML 的主要功能是 **访问数据**，因此其语法都是以**读写数据库**为主。
DML 的核心指令是 `INSERT`、`UPDATE`、`DELETE`、`SELECT`。这四个指令合称 CRUD(Create, Read, Update, Delete)，即增删改查。

事务控制语言（TCL）
事务控制语言 (Transaction Control Language, TCL) 用于**管理数据库中的事务**。这些用于管理由 DML 语句所做的更改。它还允许将语句分组为逻辑事务。
TCL 的核心指令是 `COMMIT`、`ROLLBACK`。
数据控制语言（DCL）

数据控制语言 (Data Control Language, DCL) 是一种可对数据访问权进行控制的指令，它可以控制特定用户账户对数据表、查看表、预存程序、用户自定义函数等数据库对象的控制权。
DCL 的核心指令是 `GRANT`、`REVOKE`。
DCL 以**控制用户的访问权限**为主，因此其指令作法并不复杂，可利用 DCL 控制的权限有：`CONNECT`、`SELECT`、`INSERT`、`UPDATE`、`DELETE`、`EXECUTE`、`USAGE`、`REFERENCES`

#### 增删查改

##### 视图
定义：
- 视图是基于 SQL 语句的结果集的可视化的表。
- 视图是虚拟的表，本身不包含数据，也就不能对其进行索引操作。对视图的操作和对普通表的操作一样。
作用：
- 简化复杂的 SQL 操作，比如复杂的联结；
- 只使用实际表的一部分数据；
- 通过只给用户访问视图的权限，保证数据的安全性；
- 更改数据格式和表示。
创建视图
```
CREATE VIEW top_10_user_view AS
SELECT id, username
FROM user
WHERE id < 10;
```
删除视图
```
DROP VIEW top_10_user_view;
```

#### 索引
索引是一种用于快速查询和检索数据的数据结构，其本质可以看成是一个排序好的数据接口。
**优点**：
- 使用索引可以大大加快 数据的检索速度（大大减少检索的数据量）, 这也是创建索引的最主要的原因。
- 通过创建唯一性索引，可以保证数据库表中每一行数据的唯一性。
**缺点**：
- 创建索引和维护索引需要耗费许多时间。当对表中的数据进行增删改的时候，如果数据有索引，那么索引也需要动态的修改，会降低 SQL 执行效率。
- 索引需要使用物理文件存储，也会耗费一定空间。
 创建索引
```
CREATE INDEX user_index
ON user (id);
```
添加索引
```
ALTER table user ADD INDEX user_index(id)
```
创建唯一索引
```
CREATE UNIQUE INDEX user_index
ON user (id);
```
删除索引
```
ALTER TABLE user
DROP INDEX user_index;
```

##### 约束
SQL 约束用于规定表中的数据规则。
如果存在违反约束的数据行为，行为会被约束终止。
约束可以在创建表时规定（通过 CREATE TABLE 语句），或者在表创建之后规定（通过 ALTER TABLE 语句）。
约束类型：
- `NOT NULL` - 指示某列不能存储 NULL 值。
- `UNIQUE` - 保证某列的每行必须有唯一的值。
- `PRIMARY KEY` - NOT NULL 和 UNIQUE 的结合。确保某列（或两个列多个列的结合）有唯一标识，有助于更容易更快速地找到表中的一个特定的记录。
- `FOREIGN KEY` - 保证一个表中的数据匹配另一个表中的值的参照完整性。
- `CHECK` - 保证列中的值符合指定的条件。
- `DEFAULT` - 规定没有给列赋值时的默认值。

#### 事务
不能回退 `SELECT` 语句，回退 `SELECT` 语句也没意义；也不能回退 `CREATE` 和 `DROP` 语句。
**MySQL 默认是隐式提交**，每执行一条语句就把这条语句当成一个事务然后进行提交。当出现 `START TRANSACTION` 语句时，会关闭隐式提交；当 `COMMIT` 或 `ROLLBACK` 语句执行后，事务会自动关闭，重新恢复隐式提交。
通过 `set autocommit=0` 可以取消自动提交，直到 `set autocommit=1` 才会提交；`autocommit` 标记是针对每个连接而不是针对服务器的。
指令：
- `START TRANSACTION` - 指令用于标记事务的起始点。
- `SAVEPOINT` - 指令用于创建保留点。
- `ROLLBACK TO` - 指令用于回滚到指定的保留点；如果没有设置保留点，则回退到 `START TRANSACTION` 语句处。
- `COMMIT` - 提交事务。
```
-- 开始事务
START TRANSACTION;

-- 插入操作 A
INSERT INTO `user`
VALUES (1, 'root1', 'root1', 'xxxx@163.com');

-- 创建保留点 updateA
SAVEPOINT updateA;

-- 插入操作 B
INSERT INTO `user`
VALUES (2, 'root2', 'root2', 'xxxx@163.com');

-- 回滚到保留点 updateA
ROLLBACK TO updateA;

-- 提交事务，只有操作 A 生效
COMMIT;
```

#### 权限控制

#### 存储过程

#### 游标

#### 触发器
