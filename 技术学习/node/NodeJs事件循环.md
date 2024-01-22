### NodeJs事件循环
node底层使用的语言是libuv，是一个c++语言，他是用来操作底层和操作系统，封装了操作系统接口。Node事件循环是用libuv写的，所有Node的生命周期和浏览器还是有区别的。
### 事件循环图
事件循环图：
![](../../images/Pasted%20image%2020240119150817.png)
事件循环结构图
![](../../images/Pasted%20image%2020240119150904.png)
### 主线程
![](../../images/Pasted%20image%2020240119151522.png)
上图中，几个色块的含义
- main ：启动入口文件，运行主函数
- event loop：检查是否进入事件循环
	- 检查其他线程里是否还有待处理事项
	- 检查其他任务是否还有进行中（比如计时器、文件读取操作等任务是否完成）
	- 有以上情况，进入事件循环，运行其他任务
		- 事件循环的过程：沿着从timers到close callbacks这个流程，走一圈。到event loop看是否结束，没结束再走一圈。
- over：所有的事情都完毕，结束。

### 事件循环圈
![](../../images/Pasted%20image%2020240119152015.png)
图中灰色的圈跟操作系统有关系，，不是本章解析重点。重点关注黄色、橙色的圈还有中间橘黄的方框。
我们把每一圈的事件循环叫做【一次循环】、【一次轮询】、【一次Tick】

一次循环要经过六个阶段：
1. 计时器【timers】（setTimeout、setInterval等的回调函数存放在这里）：别阶段执行已经被setTimeout（）和setInterval（）调度的回调函数。
2. 待定回调【pending callback】：执行延迟到下一个循环迭代的I/O回调。
3. idle prepare：仅系统内部使用。
4. 轮询【poll】（除了timers、check之外的回调存放在这里）：检索新的I/O实践；执行与I/O相关的回调（几乎所有情况下，除了关闭的回调函数，那些计时器和setImmediate（）调度的之外），其余情况node将在适当的时候在此阻塞。
5. 检测【check】（使用setImmediate的回调会直接进入这个队列）：setImmediate（）回调函数在这里执行。
6. 关闭的回调函数【close callbacks】：一些关闭的回调函数，如：socket.on('close',......)
#### 工作原理
- 每一个阶段都会维护一个事件队列。可以把每一个圈想象成一个事件队列。
- 这个就和浏览器不一样，浏览器最多两个队列（宏队列、微队列）。但是在node里面有六个队列
- 到达一个队列后，检查队列内是否有任务（也就是看是否有回调函数）需要执行。如果有，就依次执行，直到全部执行完毕、清空队列。
- 如果没有任务，进入下一个队列去检查。直到所有的队列都检查一遍，算一个轮询。
- 其中，timers、pending callback、idle prepare等执行完毕后，到达poll队列。

#### timers队列的工作原理
timers并非真正意义上的队列，他内部存放的是计时器。
每次到达这个队列，见检查计时器线程内的所有计时器，计时器线程内部多个计时器按照时间顺序排列。

检查过程：将没一个计时器按顺序分别计算一遍，计算该计时器开始计时的时间到当前时间是否满足计时器设定的健哥、当某个计时器检查通过，则执行回调函数。

#### poll队列的运作方式
- 如果poll中有回调函数需要执行，依次执行回调，直到清空队列。
- 如果poll中没有函数需要执行，已经是空队列了。则会在这里等待，等待其他队列（timers，pedding callbacks ，idle-prepare，checks，close-callbacks）中出现回调
	- 如果其他队列出现回调，则从poll向下到over，结束该阶段，进入下一阶段。
	- 如果其他队列也没有回调，则持续在poll队列等待，直到任何一个队列出现回调后进行工作。

#### check阶段
检查阶段（使用 setImmediate 的回调会直接进入这个队列）

##### check队列的实际工作原理：
真正的队列，里边扔的就是待执行的回调函数的集合。类似[fn,fn]这种形式的。
每次到达check这个队列后，立即按顺序执行回调函数即可
所以说，setImmediate不是一个计时器的概念。


### 举例梳理事件流程
```
setTimeout(() => {
  console.log('object');
}, 5000)
console.log('node');
```
以上代码的事件流程梳理
1. 进入主线程，执行setTimeout（），回调函数作为异步任务被放入一部队列timers队列中，暂时不执行。
2. 继续向下，执行定时器后边的console，打印node
3. 判断是否有事件循环。是，走一圈轮询：从timers-pending callback-idle prepare.....
4. 到poll队列暂停下循环并等待。
	1. 由于这个时候还没有到五秒，times队列无任务，所以一直在poll队列卡着，同事轮询检查其他队列是否有任务
5. 等5秒到达，setTimeout的回调三道timers内，例行轮询检查到timers队列的任务，则向下走，经过check、close callbacks后到达timers。将timers队列清空。
6. 继续轮询到poll等待，询问是否还有event loop，不需要，则达到over结束。

```
setTimeout(function t1() {
  console.log('setTimeout');
}, 5000)
console.log('node 生命周期');

const http = require('http')

const server = http.createServer(function h1() {
  console.log('请求回调');
});

server.listen(8080)
```
代码分析如下：
- 先执行主线程，打印“node生命周期”、引入http后创建http服务。
- 然后event-loop检查是否有异步任务，检查发现有定时器任务和请求任务。所以进入事件循环。
- 六个队列都没有任务，则在poll队列等待。
- 过了五秒，timers中有了任务，则流程从poll放行向下，经过check和close callbacks队列后，到达event loop。
- event loop检查是否有异步任务，检查发现有定时器任务和请求任务。所以再次进入事件循环。
- 到达timers队列，发现有回调任务，则依次执行回调，清空timers队列，打印出settimeout。
- 清空timers队列后，轮询继续向下到poll队列，由于poll队列现在是空队列，所以在这里等待。
- 后来，假设用户请求发来了，h1回调函数被放到poll队列。于是poll中有回调函数需要执行，依次执行回调，直到清空poll队列。
- poll队列清空，此时poll队列是空队列，继续等待。
- 由于node线程一直holding在poll队列，等很长一段时间还是没有任务来临时，会自动断开等待（不自信表现），向下执行轮询流程，经过check、close callbacks后到达event loop
- 到了event loop后，检查是否有异步任务，检查发现有请求任务。（此时定时器任务已经执行完毕，所以没有了），则继续再次进入事件循环。
- 到达poll队列，再次holding……
- 再等很长时间没有任务来临，自动断开到even loop（再补充一点无任务的循环情况）
- 再次回到poll队列挂起
- 无限循环……
![](../../images/Pasted%20image%2020240119165106.png)
```
const startTime = new Date();

setTimeout(function f1() {
  console.log('setTimeout', new Date(), new Date() - startTime);
}, 200)

console.log('node 生命周期', startTime);

const fs = require('fs')

fs.readFile('./poll.js', 'utf-8', function fsFunc(err, data) {
  const fsTime = new Date()
  console.log('fs', fsTime);
  while (new Date() - fsTime < 300) {
  }
  console.log('结束死循环', new Date());
});
```
执行流程解析：

- 执行全局上下文，打印「node 生命周期 + 时间」
- 询问是否有event loop
- 有，进入timers队列，检查没有计时器（cpu处理速度可以，这时还没到200ms）
- 轮询进入到poll，读文件还没读完（比如此时才用了20ms），因此poll队列是空的，也没有任务回调
- 在poll队列等待……不断轮询看有没有回调
- 文件读完，poll队列有了fsFunc回调函数，并且被执行，输出「fs + 时间」
- 在while死循环那里卡300毫秒，
- 死循环卡到200ms的时候，f1回调进入timers队列。但此时poll队列很忙，占用了线程，不会向下执行。
- 直到300ms后poll队列清空，输出「结束死循环 + 时间」
- event loop赶紧向下走再来一轮到timers，执行timers队列里的f1回调。于是看到「setTimeout + 时间」
- timers队列清空，回到poll队列，没有任务，等待一会。
- 等待时间够长后，向下回到event loop。
- event loop检查没有其他异步任务了，结束线程，整个程序over退出。

### setImmediate和settimeout
#### setImmediate()和settimeout(0)的对比
- setImmediate的回调是异步的，和settimeout回调性质一致。
- setImmediate回调在check队列，settimeout回调在timers队列（概念意义，实际在计时器线程，只是settimeout在timers队列做检查调用而已）
- setImmediate函数调用后，回调函数会立即push到check队里，并且在下次eventloop时会被执行。settimeout函数调用后，计时器线程增加一个定时器任务，下一次eventloop是会在timers阶段里面检查判断定时器任务是否到达时间，到了则执行回调。
- 总送，setImmediate的运算速度比settimeout(0)要快，因为settimeout需要开计时器线程，并且增加计算开销。
#### 二者效果差不多。但是执行循序不定
```
setTimeout(() => {
  console.log('setTimeout');
}, 0);

setImmediate(() => {
  console.log('setImmediate');
});

```
多次反复运行，执行效果如下：
![](../../images/Pasted%20image%2020240119171146.png)
可以看到多次运行，两句console.log打印的顺序不定。

这是因为settimeout的间隔数最小填1，虽然下边代码填了0,。但实际计算机执行当1ms算。

以上代码，主线程运行的时候，settimeout函数调用，计时器线程增加一个定时任务。setImmediate函数调用后，其回调立即push到check队列。主线程执行完毕
eventloop判断时，发现timers和check队列有内容，进入异步轮询：

第一种情况：等到了timers里这段时间，可能还没有到1ms时间，定时器任务健哥时间的条件不成立，所以timers里面还没有回调函数。继续向下到check队列，这个时候setImmediate回调函数执行。而再下一次eventloop到达timers队列，定时器到达时间，才会执行settimeout的回调任务。于是顺序就是 setImmediate->settimeout

第二种情况：但也有可能到了timers阶段是，超过了1ms。于是计算定时器条件成立，settimeout的回调函数被直接执行。eventloop再向下到达check队列执行setImmediate的回调。最终顺序就是「setTimeout -> setImmediate」了。

### process.nextTick和Promise
说完宏任务，接下来说下微任务

- 二者都是「微队列」，执行异步微任务。
- 二者不是事件循环的一部分，程序也不会开启额外的线程去处理相关任务。（理解：promise里发网络请求，那是网络请求开的网络线程，跟Promise这个微任务没关系）
- 微队列设立的目的就是让一些任务「马上」、「立即」优先执行。
- nextTick与Promise比较，nextTick的级别更高。


文章出处：https://juejin.cn/post/7010308647792148511