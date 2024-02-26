### Node模块机制
#### 请介绍一下node里的模块是什么
Node中，每个文件模块都是一个对象，它的定义如下
```
function Module(id,parent){
	this.id=id
	this.exports={}
	this.parent=parent
	this.load=false
	this.filename=null
	this.children=[]
}
module.exports=Module
var module = new Module(filename, parent);
```
#### 介绍一下require的模块加载机制
1. 先计算模块的路径
2. 如果模块在缓存内，则取出缓存
3. 如果模块不在缓存则加载模块
4. 输出模块的exports属性
```
//require 其实调用了模块内部的_load方法
Module._load=function(request,parent,isMain){
	//计算绝对路径
	var filename=Module._resoveFilename(request,parent)
	//第一步取出缓存
	var cachedModule = Module._cache[filename];
	if (cachedModule) {
		return cachedModule.exports;
	}
	//第二步判断是否为内置模块
	  if (NativeModule.exists(filename)) {
	    return NativeModule.require(filename);
	  }
	//第三部生成模块实例，存入缓存
	var module = new Module(filename, parent);
	  Module._cache[filename] = module;
	//第四部加载模块
	// 下面的module.load实际上是Module原型上有一个方法叫Module.prototype.load
	try {
	    module.load(filename);
	    hadException = false;
	  } finally {
	    if (hadException) {
	      delete Module._cache[filename];
	    }
	  }
	//第五步输出模块的exports
	return module.exports;
}
```
#### 加载模块时，为什么每个模块都有__dirname,__filename 属性呢
```
// 上面(1.2部分)的第四步module.load(filename)
// 这一步，module模块相当于被包装了，包装形式如下
// 加载js模块，相当于下面的代码（加载node模块和json模块逻辑不一样）
(function (exports, require, module, __filename, __dirname) {
  // 模块源码
  // 假如模块代码如下
  var math = require('math');
  exports.area = function(radius){
      return Math.PI * radius * radius
  }
});
```
#### node导出模块有两种方式，一种是exports.xxx=xxx和module.exports={}。这两中方式有什么区别？
- exports其实就是module.exports
- 如果要输出一个键值对象{}，可以利用exports这个已存在的空对象{}，并继续在上面添加新的键值；如果要输出一个函数或数组，必须直接对module.exports对象赋值。
```
module.exports vs exports
很多时候，你会看到，在Node环境中，有两种方法可以在一个模块中输出变量：

方法一：对module.exports赋值：

// hello.js

function hello() {
    console.log('Hello, world!');
}

function greet(name) {
    console.log('Hello, ' + name + '!');
}

module.exports = {
    hello: hello,
    greet: greet
};
方法二：直接使用exports：

// hello.js

function hello() {
    console.log('Hello, world!');
}

function greet(name) {
    console.log('Hello, ' + name + '!');
}

function hello() {
    console.log('Hello, world!');
}

exports.hello = hello;
exports.greet = greet;
但是你不可以直接对exports赋值：

// 代码可以执行，但是模块并没有输出任何变量:
exports = {
    hello: hello,
    greet: greet
};
如果你对上面的写法感到十分困惑，不要着急，我们来分析Node的加载机制：

首先，Node会把整个待加载的hello.js文件放入一个包装函数load中执行。在执行这个load()函数前，Node准备好了module变量：

var module = {
    id: 'hello',
    exports: {}
};
load()函数最终返回module.exports：

var load = function (exports, module) {
    // hello.js的文件内容
    ...
    // load函数返回:
    return module.exports;
};

var exportes = load(module.exports, module);
也就是说，默认情况下，Node准备的exports变量和module.exports变量实际上是同一个变量，并且初始化为空对象{}，于是，我们可以写：

exports.foo = function () { return 'foo'; };
exports.bar = function () { return 'bar'; };
也可以写：

module.exports.foo = function () { return 'foo'; };
module.exports.bar = function () { return 'bar'; };
换句话说，Node默认给你准备了一个空对象{}，这样你可以直接往里面加东西。

但是，如果我们要输出的是一个函数或数组，那么，只能给module.exports赋值：

module.exports = function () { return 'foo'; };
给exports赋值是无效的，因为赋值后，module.exports仍然是空对象{}。

结论
如果要输出一个键值对象{}，可以利用exports这个已存在的空对象{}，并继续在上面添加新的键值；

如果要输出一个函数或数组，必须直接对module.exports对象赋值。

所以我们可以得出结论：直接对module.exports赋值，可以应对任何情况：

module.exports = {
    foo: function () { return 'foo'; }
};
或者：

module.exports = function () { return 'foo'; };
最终，我们强烈建议使用module.exports = xxx的方式来输出模块变量，这样，你只需要记忆一种方法。
```

### node的异步I/O
#### 介绍一下node的事件循环的流程
- 在进程启动时，node会创建一个类似while(true)的循环，没执行一次循环体的过程我们称为一次Tick。
- 每个Tick的过程就是查看是否有事件待处理。如果有就取出事件及其回调函数执行。然后进入下一个循环
#### 每个tick的过程中，如何判断有事件需要处理呢
- 每个事件中有一个或者多个观察者，而判断是否有事件处理的过程就是向这些观察者询问是否有需要处理的事件。
- 事件主要来源于网络请求，文件的i/0等，这些事件对应不同的观察着
- 事件循环是一个典型的生产者/消费者模型。异步I/O，网络请求等则是事件的生产者，源源不断为Node提供不同类型的事件，这些事件被传递到对应的观察者那里，事件循环则从观察者那里取出事件并处理。
#### 请描述一下整个异步I/O的流程
![](../../images/Pasted%20image%2020240226213326.png)

### V8的垃圾回收机制
#### V8的内存限制是多少
64位系统下是1.4GB， 32位系统下是0.7GB。因为1.5GB的垃圾回收堆内存，V8需要花费50毫秒以上，做一次非增量式的垃圾回收甚至要1秒以上。这是垃圾回收中引起Javascript线程暂停执行的事件，在这样的花销下，应用的性能和影响力都会直线下降。
#### 垃圾回收算法
###### v8的垃圾回收算法
v8的垃圾回收策略主要是基于分代式垃圾回收机制。
在v8中，主要将内存分为新生代和老生代，新生代中的对象为存活时间较短的对象，老生代中的对象为存活时间较长或常驻内存的对象。
###### scavenge
新生代中的对象主要通过scavenge算法进行垃圾回收，一种采用复制方式实现的垃圾回收算法。他将堆内存分为两部分，每部分空间成为semispace。在这两个simispace空间中，只有一个处于使用，使用状态的称为from空间，空闲状态称为to空间。分配对象会在from空间中分配，当开始进行垃圾回收时，会检查from空间中的存货对象，复制到to空间，非存活对象则会被删除。然后from空间和to空间角色对换。

###### mark-sweep和mark-compact
mark-sweep是标记清除的意思，它分为标记和清除两个阶段。mark-sweep在标记阶段遍历堆中的所有对象，并标记活着的对象，在随后的清除阶段，只清除没有被标记的对象。
mark-sweep最大的问题是在进行一次标记清除后，内存空间会出现不连续的状态。这种内存碎片会对后续的内存分配造成问题，因为很有可能出现需要分配一个大对象的情况，这时所有的内存碎片空间都无法满足。就会提前触发垃圾回收

mark-compact是标记整理的意思，是在标记清除的基础上演变而来。他们的差别在于对象在标记为死亡后，在整理的过程中，将活着的对象向一端移动，移动完成后直接清理另一端的内存。

v8主要使用的是mark-sweep，在空间不足以对从新生代晋升过来的对象进行分配时，才使用mark-compact

######  Incremental Marking
为避免js逻辑应用与垃圾回收器看到的不一致的情况，垃圾回收的三种算法都需要将应用停下来，待执行完垃圾回收后再继续执行应用逻辑，这种行为被称为全停顿。

为了降低全队垃圾回收带来的停顿事件，v8先从标记阶段入手，将原本需要一口气停顿完成的动作改成增量标记，也就是拆分许多小‘步进’，每做完一个步进就让js执行一小会，垃圾回收和应用逻辑交替执行直到标记阶段完成。

### Buffer
#### 新建的Buffer会占用V8的内存么
不会，因为buffer属于堆外内存，不是v8分配的
#### Buffer.alloc和Buffer.allocUnsafe的区别
Buffer.allocUnsafe创建的 Buffer 实例的底层内存是未初始化的。 新创建的 Buffer 的内容是未知的，可能包含敏感数据。 使用 Buffer.alloc() 可以创建以零初始化的 Buffer 实例。

#### buffer的内存分配机制
为了高效的使用申请来的内存，Node采用了slab分配机制。slab是一种动态的内存管理机制。
Node以8kb为界限来来区分Buffer为大对象还是小对象，如果是小于8kb就是小Buffer，大于8kb就是大Buffer。
例如第一次分配一个1024字节的Buffer，Buffer.alloc(1024),那么这次分配就会用到一个slab，接着如果继续Buffer.alloc(1024),那么上一次用的slab的空间还没有用完，因为总共是8kb，1024+1024 = 2048个字节，没有8kb，所以就继续用这个slab给Buffer分配空间。
如果超过8kb，那么直接用C++底层地宫的SlowBuffer来给Buffer对象提供空间。
### 进程通信
#### 请简述一下node的多进程架构
面对node单线程对多核cpu使用不足的情况，Node提供了child_process模块，来实现进程的复制，node的多进程架构是主从模式。
![](../../images/Pasted%20image%2020240226214925.png)
```
var fork = require('child_process').fork;
var cpus = require('os').cpus();
for(var i = 0; i < cpus.length; i++){
    fork('./worker.js');
}
```
#### 请问创建紫禁城的方法有哪些，简单说一下他们的区别
- spawn