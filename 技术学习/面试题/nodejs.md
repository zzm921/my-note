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
}
```