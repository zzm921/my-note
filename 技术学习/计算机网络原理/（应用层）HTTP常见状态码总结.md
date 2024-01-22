HTTP 状态码用于描述 HTTP 请求的结果，比如 2xx 就代表请求被成功处理。
![[Pasted image 20240115101741.png]]
#### 1XX InFormationnal（信息性状态码）
#### 2xx Success（成功状态码）
- 200 ok：请求被成功处理。
- 201 Create：请求被成功处理并且在服务端创建了一个新的资源。比如我们通过post请求创建一个新的用户
- 202 Accepted：服务器接收请求，但还未处理
- 204 No Content：服务端已经成功处理了请求，但是没有返回任何内容。
#### 3xx Redirection（重定向状态码）
- 301 Moved Permanently：资源被永久重定向
- 302 Found：资源被零时重定向。
#### 4xx Client Error（客户端错误状态码）
- 400 Bad Request：发送的http请求存在问题。比如请求参数不合法、请求方法错误。
- 401 unauthorized：未认证请求需要认证后才能访问资源
- 403 Forbidden：直接拒绝http请求，不处理。一般用来针对非法请求
- 404 Not Found：你请求的资源未在服务端找到。
#### 5xx Server Error（服务端错误状态码）
- 500 Internal Server Error：服务端出问题了。
- 502 Bad Gateway：我们的网关请求转发到服务器，但服务返回的却是一个错误的响应。