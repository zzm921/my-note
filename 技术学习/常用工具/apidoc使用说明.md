作为后端开发，当一个服务开发完成，相对应的api接口文档也需要输出，因此写api文档也成为了工作的一部分。写过api文档的可能都会有写不出一份漂亮的api文档的苦恼。
最近有看到一个轻量级的api文档生成的工具，通过注释生成api文档。很大程度的方便我们编写和管理api文档。这就是--apidoc
#### 简介
apidoc是一款可以有源代码中的注释直接自动生成api接口文档的工具，它几乎支持目前主流的所有风格的注释。
apidoc官网 : [http://apidocjs.com/](http://apidocjs.com/)
#### 使用方法
需要安装node环境,在node环境下，通过npm安装apidoc
```
npm install apidoc -g
```
配置apidoc.json
```
    {
            "name": "alarm_server",
            "version": "0.0.1",
            "description": "闹钟服务接口文档",
            "title": "闹钟服务接口文档",
            "url": "http://localhost:3000" 
        }
```
配置package.json
```
{
  "name": "alarm_server",
  "version": "0.0.0",
  "description": "alarm_server",
  "apidoc": {
    "title": "接口文档",
    "url": "http://localhost:3000"
  }
}
```
#### api注释参数
常见注释参数如下：
```
/**
*@api {method} path [title]  定义请求api   如：  @api {get} /user/:id Users unique ID.
*@apiDefine name [title]    定义注释块
                     [description]     
*@apiDescription   text  描述
*@apiError [(group)] [{type}] field [description]  错误   
*@apiErrorExample [{type}] [title]    错误示例
                 example
*@apiExample [{type}] title    api示例
            example
*@apiGroup name   所属组
*@apiHeader [(group)] [{type}] [field=defaultValue] [description]  头部
*@apiHeaderExample [{type}] [title]    头部示例
                   example 
*@apiName text   api名字
*@apiParam [(group)] [{type}] [field=defaultValue] [description]   api参数   
*@apiParamExample [{type}] [title]   api参数示例
                   example
*@apiSuccess [(group)] [{type}] field [description]  成功返回参数
*@apiSuccessExample [{type}] [title]   成功示例
                   example
*@apiUse define   使用定义的define
*@apiVersion  版本
```
访问官方文档（[http://apidocjs.com/#params](http://apidocjs.com/#params)）可了解更多
下面是本人使用简单例子
```
/**     
* @apiDefine apiResponse    定义一个返回的模板
* @apiSuccess  {number} status 状态 0表示成功 -1表示失败
* @apiSuccess  {string} cause  状态信息
* @apiSuccess  {string} message  输出信息
*/


/**
 * @api {post} /alarm addAlarm        
 * @apiName addAlarm                   
 * @apiGroup alarm             
 * @apiVersion  0.0.1
 *
 * @apiParam  {String} startdate 闹钟开始时间
 * @apiParam  {json} ruleData 闹钟规则
 * @apiParam  {String='COUNTDOWN','ONCE','DAILY','WEEKLY','MONTHLY','YEARLY'} ruleData.repeatType 重复类型
 * @apiParam  {String} [ruleData.byminute=0] 闹钟分钟
 * @apiParam  {String} toneurl 铃声
 * @apiParam  {String} audiourl 铃声
 * @apiParam  {number} action 动作
 * @apiParam  {number} minite 持续时间
 * @apiParam  {String} alarmMessage 提醒文字
 * @apiParam  {number=0,1} [calendarType=1] 日历类型 1：公历  0：农历
 * @apiParam  {String} deviceId 设备id
 * @apiParam  {String} openid 用户openid
 *
 * @apiUse apiResponse
 *
 * @apiParamExample  {Json} Request-Example:
 * {
 *  "startdate":"20181017140000",
 *  "ruleData":{
 *      "repeatType":"once",
 *      "byonce":"20181017140000"
 *  },
 *  "toneurl":"111111",
 *  "audiourl":"111111",
 *  "action":0,
 *  "minite":30,
 *  "deviceId":"1234",
 *  "openid":"dfdfsdfsdfdsfasddf",
 *  "alarmMessage":"测试5"
 * }
 * @apiSuccessExample {type} Success-Response:
 * {
 *    "status": 0,
 *    "cause": "success",
 *    "message": "增加闹钟成功",
 *    "data": ""
 * }
 */
```
注意apiname最好不要用中文，坑死人不偿命
####生成在线文档
```
apidoc -i myapp/(路由路径) -o apidoc/(生成的api文档存放路径)
```


####后记
由此生成的是html的文档，但很多时候我们需要输出的是文件的方式，这个时候可以使用apidoc-markdown3来生成md文件，使用
```
npm install apidoc-markdown3 -g
```
安装，运行命令
```
apidoc-markdown3 -p .\public\apidoc\(apidoc生成的文档的位置) -o .\apidoc\api.md（生成md的位置）
```
使用这个方法就能生成md的api文档了，最后md转成pdf就方便多了