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
#### 每个tick