#面对对象的升序设计
##理解对象
创建对象最简单的方法
```
var person=new Object()
preson.name='dddd'
person.age=29
person.job='it'
person.sayName=function(){
console.log(this.name)
}
```
延伸
```
let person={
    name:'aaa',

    age:11,

    sayName:function(){
console.log(this.name)
}

}
```
###属性类型
ecmscript中有两种属性 数据属性和访问器属性
####数据属性
configurable  表示能否通过delete删除属性从而重新定义属性，能否修改属性的特性，或者能否吧属性修改成访问器属性。像前面的例子中那样直接在对象上定义是的属性，他们的这个特性默认值为true
enumerable 表示嫩否个通过for-in循环返回属性。像前面李中那样直接在对象上定义的属性。默认值为ture
wirtable 表示能否修改属性的值。像前面     默认值为true
value  彪悍这个属性的数据值。读取属性值的时候，从这个位置读；写入属性值的时候，把新值保存在这个位置。这只特性的默认值为undefined


修改默认属性   Object.defineProperty(obj,name,{ cibfugurable:'',enumerable :'' ,writable :'' ,value :'' })
```
var person={}    
Object.defienProperty(person,'name',{
    writable:false    

    

})
```