# params 字典

## 来源

主体取自 SecLists `Discovery/Web-Content/burp-parameter-names.txt`，
补充 40 余个高频越权、跳转、调试与文件操作参数名（`redirect_uri`、`returnUrl`、
`callback`、`filepath`、`token`、`debug` 等），剔除纯数字条目后去重共 6009 行，每行一个参数名，不含 `=`。

## 适用方位

用于隐藏参数发现与参数级漏洞探测：打越权（`id`/`role`/`uid`）、开放重定向（`url`/`next`/`return`）、
SSRF（`url`/`src`/`callback`）、文件读取与下载（`file`/`path`/`download`）、调试开关（`debug`/`test`）。
判据是参数被服务端接受后响应体差异：字段增多、长度变化、状态码从 400 变 200、
时间盲注的响应延迟，以及回显位置出现参数值反射。