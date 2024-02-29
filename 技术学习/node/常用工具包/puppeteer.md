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
- 