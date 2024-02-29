### puppeteer是什么
- Puppeteer 是 Node.js 工具引擎
- puppeteer提供了一系列的api，通过Chrome devtools protocol 协议控制Chromium/Chrome 浏览器的行为
- Puppeteer默认是以headless启动chrome的，也可以通过参数控制启动有界面的chrome
- puppeteer默认绑定了最新版的chromium版本，也可以自己指定绑定的版本
- puppeteer让我们不需要了解太多底层的cdp协议实现与浏览器的通信。
### puppeteer能做什么
- 网页截图或者生成 PDF
- 爬取 SPA 或 SSR 网站
- UI 自动化测试，模拟表单提交，键盘输入，点击等行为
- 捕获网站的时间线，帮助诊断性能问题
- 创建一个最新的自动化测试环境，使用最新的 js 和最新的 Chrome 浏览器运行测试用例
- 测试 Chrome 扩展程序
### puppeteer分层
![](../../../images/Pasted%20image%2020240229212637.png)
- browser: 对应一个浏览器实例，一个Browser可以包含多个BrowserContext
- BrowserContext：对应浏览器一个上下文回话，就像我们打开一个普通的chrome之后又打开一个隐身模式的浏览器一样，BrowserContext 具有独立的 Session(cookie 和 cache 独立不共享)，一个 BrowserContext 可以包含多个 Page。
- Page：标识一个Tab页面，通过browserContext.newPage()/browser.newPage()创建，browser.newPage() 创建页面时会使用默认的 BrowserContext，一个 Page 可以包含多个 Frame
- Frame：一个框架，每个页面都有一个主框架(page,MainFrame()),也可以多个子框架，主要由iframe标签创建产生
- executionContext:是js的执行环境，每一个Frame都有一个默认的js执行环境
- ElementHandle：对应DOM的一个元素节点，通过该实例可以实现对元素的点击，填写表单等行为，我们可以通过选择器，xPath等来获取对应的元素。
- JSHandle：对应dom中的js对象，elementHandle继承与jshandle，由于我们无法直接操作dom对象，所以封装成jshandle来实现相关功能。
- CDPSession：可以直接与原生的 CDP 进行通信，通过 session.send 函数直接发消息，通过 session.on 接收消息，可以实现 Puppeteer API 中没有涉及的功能
- Coverage：获取 JavaScript 和 CSS 代码覆盖率
- Tracing：抓取性能数据进行分析
- Response： 页面收到的响应
- Request： 页面发出的请求

### 如何创建一个Browser实例
- puppeteer.connect:连接一个已经存在的chrome实例
- puppeteer.launch:每次都启动一个chrome实例
```
let browser =await puppeteer.launch({
	headless:false,//有浏览器界面启动
	slowMo:100,//放慢浏览器执行速度，方便测试观察
	args:[
		'-no-sandbox',
        '--window-size=1280,960'
	],
})
let page =await browser.newPage()
await page.goto('xxxxx')
await page.close()
await borwser.close()


```