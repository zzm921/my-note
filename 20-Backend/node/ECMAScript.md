1、let , const ,var
    const 常量

    let 块级变量

    var定义的是顶层变量


浏览器里面，顶层对象是 window ，但 Node 和 Web Worker 没有 window 。
浏览器和 Web Worker 里面， self 也指向顶层对象，但是 Node 没有 self 。
Node 里面，顶层对象是 global ，但其他环境都不支持。
2、解构