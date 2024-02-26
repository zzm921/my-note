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
Module._load=function(request,parent,isMain)
```