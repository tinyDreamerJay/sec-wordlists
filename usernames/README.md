# usernames 字典

## 来源

整理自 SecLists `Usernames/` 的 `top-usernames-shortlist.txt`、`cirt-default-usernames.txt`
与 `xato-net-10-million-usernames-dup.txt` 的前段，补充常见服务账号（`tomcat`、`jenkins`、
`postgres`、`sa`、`deploy` 等），转小写、不区分大小写去重，截断至 20000 行。

## 适用方位

用于账号枚举与撞库组合：先确认用户名是否存在（注册、找回密码、登录报错的差异），
再用 `passwords/` 做组合。判据是「用户不存在」与「密码错误」两类响应的文案、状态码、
响应时间或用例前缀差异；接口有频率限制时按阈值降速并轮换来源。