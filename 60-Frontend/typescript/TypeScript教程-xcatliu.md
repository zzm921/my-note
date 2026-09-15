---
type: tutorial
domain: frontend/typescript
tags: [TypeScript, 类型系统, 教程, xcatliu]
status: done
source: https://ts.xcatliu.com/
created: 2026-09-16
updated: 2026-09-16
---

# TypeScript 教程（xcatliu）

> 本文由原 `1基础` / `2声明文件` / `3内置对象` / `4进阶` 四篇碎片合并而成，
> 内容来源：[TypeScript 入门教程](https://ts.xcatliu.com/)。

## 目录

- [一、基础篇](#一基础篇)
- [二、声明文件](#二声明文件)
- [三、内置对象](#三内置对象)
- [四、进阶篇](#四进阶篇)
- [附：类 · 学习大纲](#附类--学习大纲)

---

## 一、基础篇

#### 何谈重识
何谈重识，重新认识，重新学习。以前用过typescript，年少不识其真面目，只知道使用一些简单的语法。没有深入去看过。后面使用了js，发现了其不足。故返程学习typescript。
参考地址
https://ts.xcatliu.com/introduction/what-is-typescript.html
#### 安装（已安装node环境）
    npm install -g typescript

以上命令会在全局环境下安装 tsc 命令，安装完成之后，我们就可以在任何地方执行 tsc 命令了,如`tsc hello.ts`则变异了hello.ts文件


##### export
```
export { name1, name2, …, nameN };
export { variable1 as name1, variable2 as name2, …, nameN };
export let name1, name2, …, nameN; // also var
export let name1 = …, name2 = …, …, nameN; // also var, const


export default expression;
export default function (…) { … } // also class, function*
export default function name1(…) { … } // also class, function*
export { name1 as default, … };


export * from …;
export { name1, name2, …, nameN } from …;
export { import1 as name1, import2 as name2, …, nameN } from …;
```


### 原始数据类型
js类型分为两种：原始数据类型，对象数据类型
原始数据类型包括
- 布尔值
- 数值
- 字符串
- null
- undefined
- es6中的新类型 Synbol
- es10中的新类型 BigInt

```
//布尔值
let isDone :boolean=false //布尔值

let createdByNewBoolean: boolean = new Boolean(1); //对象创建的不是布尔值，而是一个对象

// 数值
let decLiteral: number = 6;
let hexLiteral: number = 0xf00d;
// ES6 中的二进制表示法
let binaryLiteral: number = 0b1010;
// ES6 中的八进制表示法
let octalLiteral: number = 0o744;
let notANumber: number = NaN;
let infinityNumber: number = Infinity;

// 字符串
let myName: string = 'Tom';
let myAge: number = 25;

// 模板字符串
let sentence: string = `Hello, my name is ${myName}.
I'll be ${myAge + 1} years old next month.`;


// 空值

JavaScript 没有空值（Void）的概念，在 TypeScript 中，可以用 `void` 表示没有任何返回值的函数：

function alertName(): void {
    alert('My name is Tom');
}

声明一个 `void` 类型的变量没有什么用，因为你只能将它赋值为 `undefined` 和 `null`（只在 --strictNullChecks 未指定时）：

let unusable: void = undefined;

// ## Null 和 Undefined

let u: undefined = undefined;
let n: null = null;

```

### 任意值
任意值(any)用来标识允许赋值为任意类型

### 类型推论
如果没有明确的指定类型，那么 TypeScript 会依照类型推论（Type Inference）的规则推断出一个类型。


```ts
let myFavoriteNumber = 'seven';
myFavoriteNumber = 7;

// index.ts(2,1): error TS2322: Type 'number' is not assignable to type 'string'.
```

**如果定义的时候没有赋值，不管之后有没有赋值，都会被推断成 `any` 类型而完全不被类型检查**：
```ts
let myFavoriteNumber;
myFavoriteNumber = 'seven';
myFavoriteNumber = 7;
```

### 联合类型
联合类型（Union Types）表示取值可以为多种类型中的一种。
```ts
let myFavoriteNumber: string | number;
myFavoriteNumber = 'seven';
myFavoriteNumber = 7;
```
联合类型使用 `|` 分隔每个类型。

##### 访问联合类型的属性或方法
当 TypeScript 不确定一个联合类型的变量到底是哪个类型的时候，我们**只能访问此联合类型的所有类型里共有的属性或方法**
```ts
function getLength(something: string | number): number {
    return something.length;
}

// index.ts(2,22): error TS2339: Property 'length' does not exist on type 'string | number'.
//   Property 'length' does not exist on type 'number'.

如果要可以使用，需要指定类型用as

```

### 对象的类型---接口
ts中，使用接口(Interface)来定义对象的类型。除了可用于[对类的一部分行为进行抽象](https://ts.xcatliu.com/advanced/class-and-interfaces.html#%E7%B1%BB%E5%AE%9E%E7%8E%B0%E6%8E%A5%E5%8F%A3)以外，也常用于对「对象的形状（Shape）」进行描述。
```
interface Person{
	name:string;
	age:number;
}

let tom:presong={
	name:'tom',
	age:25
}
```
定义的变量比定义的接口多或少属性都不允许。**赋值的时候，变量的形状必须和接口的形状保持一致**。

#### 可选属性
```ts
interface Person {
    name: string;
    age?: number;
}

let tom: Person = {
    name: 'Tom'
};
```

#### 任意属性
```ts
interface Person {
    name: string;
    age?: number;
    [propName: string]: any;
}

let tom: Person = {
    name: 'Tom',
    gender: 'male'
};
```
**一旦定义了任意属性，那么确定属性和可选属性的类型都必须是它的类型的子集**

#### 只读属性
有时候我们希望对象中的一些字段只能在创建的时候被赋值，那么可以用 `readonly` 定义只读属性
```ts
interface Person {
    readonly id: number;
    name: string;
    age?: number;
    [propName: string]: any;
}

let tom: Person = {
    id: 89757,
    name: 'Tom',
    gender: 'male'
};

tom.id = 9527;

// index.ts(14,5): error TS2540: Cannot assign to 'id' because it is a constant or a read-only property.
```

### 数组类型
#### [类型+方括号]表示法
```ts
let fibonacci: number[] = [1, 1, 2, 3, 5]; //数组中的类型必须为number
```
#### 数组泛型
```ts
let fibonacci: Array<number> = [1, 1, 2, 3, 5];
```
#### 用接口表示数组
```
interface NumArray{
	[index:number]:number
}
let fibonacci: NumberArray = [1, 1, 2, 3, 5];
```
`NumberArray` 表示：只要索引的类型是数字时，那么值的类型必须是数字。一般不试用
#### 类数组
#### 任意类型数组
```
let list:any[]=['a',1,2,null]
```

### 函数类型
```ts
//函数声明
function sum(x: number, y: number): number {
    return x + y;
}

//函数表达式
let mySum = function (x: number, y: number): number {
    return x + y;
};

//注意不要混淆了 TypeScript 中的 `=>` 和 ES6 中的 `=>`。

//在 TypeScript 的类型定义中，`=>` 用来表示函数的定义，左边是输入类型，需要用括号括起来，右边是输出类型。

```
#### 用接口定义函数的形状
```ts 
interface SearchFunc{
	(source:string,subString:string):boolean;
}

let mySearch: SearchFunc;
mySearch = function(source: string, subString: string) {
    return source.search(subString) !== -1;
}
```

#### 可选参数
可选参数后面加`?`号
可选参数必须接在必需参数后面。换句话说，**可选参数后面不允许再出现必需参数了**

#### 参数默认值
#### 剩余参数
使用 `...rest` 的方式获取函数中的剩余参数
#### 重载
```ts
function reverse(x: number): number;
function reverse(x: string): string;
function reverse(x: number | string): number | string | void {
    if (typeof x === 'number') {
        return Number(x.toString().split('').reverse().join(''));
    } else if (typeof x === 'string') {
        return x.split('').reverse().join('');
    }
}
//TypeScript 会优先从最前面的函数定义开始匹配，所以多个函数定义如果有包含关系，需要优先把精确的定义写在前面。
```

### 类型断言【todo】
类型断言（Type Assertion）可以用来手动指定一个值的类型。

#### 语法
```ts
值 as 类型
```
或
```ts
<类型>值
```

---

## 二、声明文件

### 声明文件
当使用第三方库时，我们需要引用它的声明文件，才能获得对应的代码补全、接口提示等功能。
### 语法索引
-   [`declare var`](https://ts.xcatliu.com/basics/declaration-files.html#declare-var) 声明全局变量
-   [`declare function`](https://ts.xcatliu.com/basics/declaration-files.html#declare-function) 声明全局方法
-   [`declare class`](https://ts.xcatliu.com/basics/declaration-files.html#declare-class) 声明全局类
-   [`declare enum`](https://ts.xcatliu.com/basics/declaration-files.html#declare-enum) 声明全局枚举类型
-   [`declare namespace`](https://ts.xcatliu.com/basics/declaration-files.html#declare-namespace) 声明（含有子属性的）全局对象
-   [`interface` 和 `type`](https://ts.xcatliu.com/basics/declaration-files.html#interface-%E5%92%8C-type) 声明全局类型
-   [`export`](https://ts.xcatliu.com/basics/declaration-files.html#export) 导出变量
-   [`export namespace`](https://ts.xcatliu.com/basics/declaration-files.html#export-namespace) 导出（含有子属性的）对象
-   [`export default`](https://ts.xcatliu.com/basics/declaration-files.html#export-default) ES6 默认导出
-   [`export =`](https://ts.xcatliu.com/basics/declaration-files.html#export-1) commonjs 导出模块
-   [`export as namespace`](https://ts.xcatliu.com/basics/declaration-files.html#export-as-namespace) UMD 库声明全局变量
-   [`declare global`](https://ts.xcatliu.com/basics/declaration-files.html#declare-global) 扩展全局变量
-   [`declare module`](https://ts.xcatliu.com/basics/declaration-files.html#declare-module) 扩展模块
-   [`/// <reference />`](https://ts.xcatliu.com/basics/declaration-files.html#san-xie-xian-zhi-ling) 三斜线指令

## 什么是声明语句[§](https://ts.xcatliu.com/basics/declaration-files.html#%E4%BB%80%E4%B9%88%E6%98%AF%E5%A3%B0%E6%98%8E%E8%AF%AD%E5%8F%A5)

假如我们想使用第三方库 jQuery，一种常见的方式是在 html 中通过 `<script>` 标签引入 jQuery，然后就可以使用全局变量 `$` 或 `jQuery` 了。

我们通常这样获取一个 `id` 是 `foo` 的元素：

```js
$('#foo');
// or
jQuery('#foo');
```

但是在 ts 中，编译器并不知道 `$` 或 `jQuery` 是什么东西[1](https://github.com/xcatliu/typescript-tutorial/tree/master/examples/declaration-files/01-jquery)：

```ts
jQuery('#foo');
// ERROR: Cannot find name 'jQuery'.
```

这时，我们需要使用 `declare var` 来定义它的类型[2](https://github.com/xcatliu/typescript-tutorial/tree/master/examples/declaration-files/02-declare-var)：

```ts
declare var jQuery: (selector: string) => any;

jQuery('#foo');
```

上例中，`declare var` 并没有真的定义一个变量，只是定义了全局变量 `jQuery` 的类型，仅仅会用于编译时的检查，在编译结果中会被删除。它编译结果是：

```js
jQuery('#foo');
```

### 什么是声明文件
通常我们会把声明语句放到一个单独的文件中(xxx.d.ts),声明文件必需以 `.d.ts` 为后缀。

### 第三方声明文件
使用@types统一管理第三方库的声明文件
```bash
npm install @types/jquery --save-dev
```

### 书写声明文件
当一个第三方库没有提供声明文件时，我们就需要自己书写声明文件了。
库的使用场景主要有以下几种：
-   [全局变量](https://ts.xcatliu.com/basics/declaration-files.html#quan-ju-bian-liang)：通过 `<script>` 标签引入第三方库，注入全局变量
-   [npm 包](https://ts.xcatliu.com/basics/declaration-files.html#npm-bao)：通过 `import foo from 'foo'` 导入，符合 ES6 模块规范
-   [UMD 库](https://ts.xcatliu.com/basics/declaration-files.html#umd-ku)：既可以通过 `<script>` 标签引入，又可以通过 `import` 导入
-   [直接扩展全局变量](https://ts.xcatliu.com/basics/declaration-files.html#zhi-jie-kuo-zhan-quan-ju-bian-liang)：通过 `<script>` 标签引入后，改变一个全局变量的结构
-   [在 npm 包或 UMD 库中扩展全局变量](https://ts.xcatliu.com/basics/declaration-files.html#zai-npm-bao-huo-umd-ku-zhong-kuo-zhan-quan-ju-bian-liang)：引用 npm 包或 UMD 库后，改变一个全局变量的结构
-   [模块插件](https://ts.xcatliu.com/basics/declaration-files.html#mo-kuai-cha-jian)：通过 `<script>` 或 ` 


#### declare var
在所有的声明语句中，`declare var` 是最简单的，如之前所学，它能够用来定义一个全局变量的类型。与其类似的，还有 `declare let` 和 `declare const`，使用 `let` 与使用 `var` 没有什么区别：

```ts
// src/jQuery.d.ts

declare let jQuery: (selector: string) => any;
```

```ts
// src/index.ts

jQuery('#foo');
// 使用 declare let 定义的 jQuery 类型，允许修改这个全局变量
jQuery = function(selector) {
    return document.querySelector(selector);
};
```
而当我们使用 `const` 定义时，表示此时的全局变量是一个常量，不允许再去修改它的值了[4](https://github.com/xcatliu/typescript-tutorial/tree/master/examples/declaration-files/04-declare-const-jquery)：

```ts
// src/jQuery.d.ts

declare const jQuery: (selector: string) => any;

jQuery('#foo');
// 使用 declare const 定义的 jQuery 类型，禁止修改这个全局变量
jQuery = function(selector) {
    return document.querySelector(selector);
};
// ERROR: Cannot assign to 'jQuery' because it is a constant or a read-only property.
```

#### declare function
定义全局函数类型
```ts
// src/jQuery.d.ts

declare function jQuery(selector: string): any;
```

```ts
// src/index.ts

jQuery('#foo');
```

函数类型的声明支持重载

```ts
// src/jQuery.d.ts

declare function jQuery(selector: string): any;
declare function jQuery(domReadyCallback: () => any): any;
```

#### declare class
全局变量为一个类时定义，只能定义类型，不能用来定义具体的实现
```ts
// src/Animal.d.ts

declare class Animal {
    name: string;
    constructor(name: string);
    sayHi(): string;
}
```

```ts
// src/index.ts

let cat = new Animal('Tom');
```

#### declare  enum
定义枚举类型，也称作外部枚举
```ts
// src/Directions.d.ts

declare enum Directions {
    Up,
    Down,
    Left,
    Right
}
```

```ts
// src/index.ts

let directions = [Directions.Up, Directions.Down, Directions.Left, Directions.Right];
```

#### declare namespace
用来表示全局变量是一个对象，包含很多子属性。
比如 `jQuery` 是一个全局变量，它是一个对象，提供了一个 `jQuery.ajax` 方法可以调用，那么我们就应该使用 `declare namespace jQuery` 来声明这个拥有多个子属性的全局变量。

```ts
// src/jQuery.d.ts

declare namespace jQuery {
    function ajax(url: string, settings?: any): void;
}
```

```ts
// src/index.ts

jQuery.ajax('/api/get_something');
```
注意，在 `declare namespace` 内部，我们直接使用 `function ajax` 来声明函数，而不是使用 `declare function ajax`。类似的，也可以使用 `const`, `class`, `enum` 等语句[9](https://github.com/xcatliu/typescript-tutorial/tree/master/examples/declaration-files/09-declare-namespace)

##### 防止命名冲突[§](https://ts.xcatliu.com/basics/declaration-files.html#%E9%98%B2%E6%AD%A2%E5%91%BD%E5%90%8D%E5%86%B2%E7%AA%81)

暴露在最外层的 `interface` 或 `type` 会作为全局类型作用于整个项目中，我们应该尽可能的减少全局变量或全局类型的数量。故最好将他们放到 `namespace` 下[13](https://github.com/xcatliu/typescript-tutorial/tree/master/examples/declaration-files/13-avoid-name-conflict)：

```ts
// src/jQuery.d.ts

declare namespace jQuery {
    interface AjaxSettings {
        method?: 'GET' | 'POST'
        data?: any;
    }
    function ajax(url: string, settings?: AjaxSettings): void;
}
```

注意，在使用这个 `interface` 的时候，也应该加上 `jQuery` 前缀：

```ts
// src/index.ts

let settings: jQuery.AjaxSettings = {
    method: 'POST',
    data: {
        name: 'foo'
    }
};
jQuery.ajax('/api/post_something', settings);
```


### npm包
一般我们通过`import foo from 'foo'`导入一个npm包，通常npm包的声明文件可能存在于两个地方:
- 和npm包绑定在一起，判断依据是 `package.json` 中有 `types` 字段，或者有一个 `index.d.ts` 声明文件。
- 发布到@types里。我们只需要尝试安装一下对应的 `@types` 包就知道是否存在该声明文件，安装命令是 `npm install @types/foo --save-dev`。这种模式一般是由于 npm 包的维护者没有提供声明文件，所以只能由其他人将声明文件发布到 `@types` 里了。
如果两种方式都没有找到对应的声明文件，则需要自己创建。两种方法：
- 创建一个`node_modules/@types/foo/index.d.ts` 文件，存放 `foo` 模块的声明文件。不推荐
- 创建一个 `types` 目录，专门用来管理自己写的声明文件，将 `foo` 的声明文件放到 `types/foo/index.d.ts` 中。这种方式需要配置下 `tsconfig.json` 中的 `paths` 和 `baseUrl` 字段。

目录结构：

```autoit
/path/to/project
├── src
|  └── index.ts
├── types
|  └── foo
|     └── index.d.ts
└── tsconfig.json
```

`tsconfig.json` 内容：

```json
{
    "compilerOptions": {
        "module": "commonjs",
        "baseUrl": "./",
        "paths": {
            "*": ["types/*"]
        }
    }
}
```

npm包的声明文件有已下几种语法
-   [`export`](https://ts.xcatliu.com/basics/declaration-files.html#export) 导出变量
-   [`export namespace`](https://ts.xcatliu.com/basics/declaration-files.html#export-namespace) 导出（含有子属性的）对象
-   [`export default`](https://ts.xcatliu.com/basics/declaration-files.html#export-default) ES6 默认导出
-   [`export =`](https://ts.xcatliu.com/basics/declaration-files.html#export-1) commonjs 导出模块


#### `export`[§](https://ts.xcatliu.com/basics/declaration-files.html#export)

npm 包的声明文件与全局变量的声明文件有很大区别。在 npm 包的声明文件中，使用 `declare` 不再会声明一个全局变量，而只会在当前文件中声明一个局部变量。只有在声明文件中使用 `export` 导出，然后在使用方 `import` 导入后，才会应用到这些类型声明。

##### 混用 `declare` 和 `export`[§](https://ts.xcatliu.com/basics/declaration-files.html#%E6%B7%B7%E7%94%A8-declare-%E5%92%8C-export)

我们也可以使用 `declare` 先声明多个变量，最后再用 `export` 一次性导出


#### `export namespace`[§](https://ts.xcatliu.com/basics/declaration-files.html#export-namespace)

与 `declare namespace` 类似，`export namespace` 用来导出一个拥有子属性的对象

#### `export default`[§](https://ts.xcatliu.com/basics/declaration-files.html#export-default)

在 ES6 模块系统中，使用 `export default` 可以导出一个默认值，使用方可以用 `import foo from 'foo'` 而不是 `import { foo } from 'foo'` 来导入这个默认值

#### `export =`[§](https://ts.xcatliu.com/basics/declaration-files.html#export-)

在 commonjs 规范中，我们用以下方式来导出一个模块：

```js
// 整体导出
module.exports = foo;
// 单个导出
exports.bar = bar;
```

在 ts 中，针对这种模块导出，有多种方式可以导入，第一种方式是 `const ... = require`：

```js
// 整体导入
const foo = require('foo');
// 单个导入
const bar = require('foo').bar;
```

第二种方式是 `import ... from`，注意针对整体导出，需要使用 `import * as` 来导入：

```ts
// 整体导入
import * as foo from 'foo';
// 单个导入
import { bar } from 'foo';
```

第三种方式是 `import ... require`，这也是 ts 官方推荐的方式：

```ts
// 整体导入
import foo = require('foo');
// 单个导入
import bar = foo.bar;
```

对于这种使用 commonjs 规范的库，假如要为它写类型声明文件的话，就需要使用到 `export =` 这种语法了[21](https://github.com/xcatliu/typescript-tutorial/tree/master/examples/declaration-files/21-export-equal)：

```ts
// types/foo/index.d.ts

export = foo;

declare function foo(): string;
declare namespace foo {
    const bar: number;
}
```

需要注意的是，上例中使用了 `export =` 之后，就不能再单个导出 `export { bar }` 了。所以我们通过声明合并，使用 `declare namespace foo` 来将 `bar` 合并到 `foo` 里。
不推荐使用

---

## 三、内置对象

### 内置对象
#### ECMAScript 内置对象
Boolean  Error  Date  RegExp

```ts
let b: Boolean = new Boolean(1);
let e: Error = new Error('Error occurred');
let d: Date = new Date();
let r: RegExp = /[a-z]/;
```

#### DOM和BOM内置对象
`Document`、`HTMLElement`、`Event`、`NodeList`

```ts
et body: HTMLElement = document.body;
let allDiv: NodeList = document.querySelectorAll('div');
document.addEventListener('click', function(e: MouseEvent) {
  // Do something
});
```

#### TypeScript 核心库的定义文件
[TypeScript 核心库的定义文件](https://github.com/Microsoft/TypeScript/tree/master/src/lib)中定义了所有浏览器环境需要用到的类型，并且是预置在 TypeScript 中的。

#### TypeScript写node.js
安装@types/node

```bash
npm install @types/node --save-dev
```

---

## 四、进阶篇

### 类型别名
类型别名用来给一个类型起个新名字

```ts
type Name = string;
type NameResolver = () => string;
type NameOrResolver = Name | NameResolver;
function getName(n: NameOrResolver): Name {
    if (typeof n === 'string') {
        return n;
    } else {
        return n();
    }
}
```
上例中，我们使用 `type` 创建类型别名。

类型别名常用于联合类型。

### 字符串字面量类型
字符串字面量类型用来约束取值只能是某几个字符串中的一个

```ts
type EventNames = 'click' | 'scroll' | 'mousemove';
function handleEvent(ele: Element, event: EventNames) {
    // do something
}

handleEvent(document.getElementById('hello'), 'scroll');  // 没问题
handleEvent(document.getElementById('world'), 'dblclick'); // 报错，event 不能为 'dblclick'

// index.ts(7,47): error TS2345: Argument of type '"dblclick"' is not assignable to parameter of type 'EventNames'.
```

使用type定义了一个字符串字面量类型 EventNames，该类型的值只能取定义的三个值

### 元组
数组合并了相同类型的对象，而元组（tuple）合并了不同类型的对象
```ts
let tom: [string, number] = ['Tom', 25];
```

#### 越界的元素
当添加越界的元素时，它的类型会被限制为元组中每个类型的联合类型：
```ts
let tom: [string, number];
tom = ['Tom', 25];
tom.push('male');
tom.push(true);

// Argument of type 'true' is not assignable to parameter of type 'string | number'.
```

### 枚举
枚举（Enum）类型用于取值被限定在一定范围内的场景，比如一周只能有七天，颜色限定为红绿蓝等。

```ts
enum Days {Sun, Mon, Tue, Wed, Thu, Fri, Sat};
```

枚举成员会被赋值为从 `0` 开始递增的数字，同时也会对枚举值到枚举名进行反向映射。

同时也能手动复制

```ts
enum Days {Sun = 7, Mon = 1, Tue, Wed, Thu, Fri, Sat};

console.log(Days["Sun"] === 7); // true
console.log(Days["Mon"] === 1); // true
console.log(Days["Tue"] === 2); // true
console.log(Days["Sat"] === 6); // true
```

#### 常数项和计算所得项

```ts
enum Color {Red, Green, Blue = "blue".length};
```

上面的例子中，`"blue".length` 就是一个计算所得项。
计算所得项后面的值必须是手动赋值的项


当满足以下条件时，枚举成员被当作是常数：

-   不具有初始化函数并且之前的枚举成员是常数。在这种情况下，当前枚举成员的值为上一个枚举成员的值加 `1`。但第一个枚举元素是个例外。如果它没有初始化方法，那么它的初始值为 `0`。
-   枚举成员使用常数枚举表达式初始化。常数枚举表达式是 TypeScript 表达式的子集，它可以在编译阶段求值。当一个表达式满足下面条件之一时，它就是一个常数枚举表达式：
    -   数字字面量
    -   引用之前定义的常数枚举成员（可以是在不同的枚举类型中定义的）如果这个成员是在同一个枚举类型中定义的，可以使用非限定名来引用
    -   带括号的常数枚举表达式
    -   `+`, `-`, `~` 一元运算符应用于常数枚举表达式
    -   `+`, `-`, `*`, `/`, `%`, `<<`, `>>`, `>>>`, `&`, `|`, `^` 二元运算符，常数枚举表达式做为其一个操作对象。若常数枚举表达式求值后为 NaN 或 Infinity，则会在编译阶段报错

#### 常数枚举
常数枚举是使用`const enum`定义的枚举类型
```ts
const enum Directions {
    Up,
    Down,
    Left,
    Right
}

let directions = [Directions.Up, Directions.Down, Directions.Left, Directions.Right];
```

常数枚举与普通枚举的区别是，它会在编译阶段被删除，并且不能包含计算成员。

上例的编译结果是：

```js
var directions = [0 /* Up */, 1 /* Down */, 2 /* Left */, 3 /* Right */];
```

#### 外部枚举
外部枚举（Ambient Enums）是使用 `declare enum` 定义的枚举类型：
```ts
declare enum Directions {
    Up,
    Down,
    Left,
    Right
}

let directions = [Directions.Up, Directions.Down, Directions.Left, Directions.Right];
```
之前提到过，`declare` 定义的类型只会用于编译时的检查，编译结果中会被删除。

上例的编译结果是：

```js
var directions = [Directions.Up, Directions.Down, Directions.Left, Directions.Right];
```

外部枚举与声明语句一样，常出现在声明文件中。

同时使用 `declare` 和 `const` 也是可以的：

```ts
declare const enum Directions {
    Up,
    Down,
    Left,
    Right
}

let directions = [Directions.Up, Directions.Down, Directions.Left, Directions.Right];
```

编译结果：

```js
var directions = [0 /* Up */, 1 /* Down */, 2 /* Left */, 3 /* Right */];
```

---

## 附：类 · 学习大纲

> 以下为原始学习大纲草稿（OOP 概念速览）。完整讲解见 [[基础知识]] 的「类」章节。

- 类：定义了一件事物的抽象特点，包含它的属性和方法
- 对象 ：类的示例，通过new生成
- 面对对象的三大特性：封装、继承、多台
- 封装：对数据的操作细节隐藏起来，只暴露对外的接口。外接调用端不需要知道细节，就能同各国对外提供的接口来访问该对象，同事也保证了外接无法任意改变对象内部的数据
- 继承：子类继承父类，子类除了拥有父类所有特性外，还有一些更具体的特性
- 多台：有继承而产生了相关的不同的类，对同一个方法可以有不同的相应。
- 存取器：用以改变属性的读取和复制行为
- 修饰符：修饰符是一些关键词，用于限定成员或类型的性质。如public表示公有属性或方法
- 抽象类：抽象类是供其他类继承的基类，抽象类不允许被实例化。抽象类中的抽象方法必须在子类中被实现
- 接口：不同类之间共有的属性或方法，可以抽象成一个接口。接口可以被类实现。一个类智能集成自另一个类，但可以实现多个接口。
