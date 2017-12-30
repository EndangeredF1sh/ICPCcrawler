# ICPCcrawler - 比赛监控程序
基于Python3的一个轻量的，HUSTOJ平台比赛的监控程序。
主要用于主办方的气球配送管理。
## 依赖
* requests
## 快速开始
修改ICPCcrawler.py文件进行配置。需修改的参数如下：
* urllogin —— 填入监控的HUSTOJ的登录页面地址
* urlstatus —— 填入待监控比赛的status/状态界面地址
* data —— 填入可登录所需平台的账号和密码以及相应的Referer
* pattern（可选）—— 修改正则表达式获取个性化结果
## To Do List
* 增加可视化界面 初步计划采用web方式实现
## 已通过测试平台
* macOS 10.13.2
* Windows暂未测试
## 交流
* EndangeredFish <zwy346545141@gmail.com>
* LucienShui <lucienshui.outlook.com>
* 在issue中提出意见