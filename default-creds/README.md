# default-creds 字典

## 来源

主体为 SecLists `Passwords/Default-Credentials/` 下的 `tomcat-betterdefaultpasslist.txt`、
`ssh-betterdefaultpasslist.txt`、`mysql-betterdefaultpasslist.txt`、`ftp-betterdefaultpasslist.txt`，
合并后剔除注释、不区分大小写去重，并补充 20 组数据库与中间件默认口令，共 282 行，格式 `user:pass`。

## 适用方位

用于默认凭据尝试：打 Tomcat Manager、Weblogic、Jenkins、SSH/FTP/MySQL 等暴露的管理入口，
以及设备与控制台的出厂账号。判据是登录成功后的会话 Cookie、管理页标题、
服务端 banner 或数据库连接成功后的版本回显；同一目标上先试与 banner 匹配的组件条目再扩散。