vscode +eslint
https://www.zhihu.com/question/52777843
作者：纵横
链接：https://www.zhihu.com/question/52777843/answer/254858534
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


定制化的格式化

vs code的配置文件:

按照下面这幅图操作，vs code会打开一个json配置文件。

format相关:

搜索format，你会看到很多默认的格式化配置项。

更改format配置

你可以选择想要更改的内容，复制到右边进行更改，当然，有些配置项是装好插件才会出来的。 后面所说的设置配置文件都是修改右边这里哦～

安装插件:

非常简单咯，点击左侧图标，然后输入你想搜索的名字就好了。当然有些插件可能没有被官方采纳。你也可以去github上下载。

所以:

你想要一个什么样的格式化基本上都可以实现，阅读一下不同插件的github里面的readme就可以了。 ESLint格式化

如果题主认真读了 ESLint的Readme 的话，应该可以写出下面的配置了。不过我还是写一下好了。

安装插件：
ESLint


用来格式化和提示格式错误。

设置文件类型:

设置配置:

{
  "workbench.startupEditor": "welcomePage",
  "editor.tabSize": 2,
  "eslint.autoFixOnSave": true,
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    {
      "language": "html",
      "autoFix": true
    },
    {
      "language": "vue",
      "autoFix": true
    }
  ]
} 在Vue项目中的ESLint

其实在工作中，我们往往不喜欢常常去按保存键，或者在保存之前想先格式化一下再继续写。

因此，我采用了下面的方式：

安装插件：
Vetur


默认自带了格式化的功能，快捷键是shift+option+f（mac）。主要用来格式化复制粘贴的代码。
ESLint


在编码过程中提示格式错误，养成良好的编码习惯。

设置文件类型:

设置配置：

{
  "workbench.startupEditor": "welcomePage",
  "vetur.format.defaultFormatter.js": "vscode-typescript",
  "javascript.format.insertSpaceBeforeFunctionParenthesis": true,
  "editor.quickSuggestions": {
    "strings": true
  },
  "editor.tabSize": 2,
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "html",
    "vue",
    {
      "language": "html",
      "autoFix": true
    }
  ]
} 在JS中的格式化

在工作中发现Standard Style很符合ESLint的要求，因此JS的格式化就选用了这个插件。

安装插件：
Javascript Standard Style


设置文件类型: