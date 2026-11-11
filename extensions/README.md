# extensions 字典

## 来源

以 SecLists `Discovery/Web-Content/web-extensions.txt` 为基线，补充动态脚本（`php7`、`phtml`、
`ashx`、`jspx`）、备份与临时后缀（`bak`、`old`、`swp`、`save`）、归档（`zip`、`tar`、`gz`、`7z`）、
密钥与证书（`pem`、`key`、`pfx`、`jks`）等常见后缀，统一去掉开头的点、去重后共 114 行，每行一个后缀。

## 适用方位

用于后缀碰撞：已知文件名时猜备份与编辑器残留（`index.php.bak`、`config.php~`）、
上传点判断哪些后缀可解析、静态资源目录里找源码与配置副本。
判据是拼接后的状态码与内容类型变化（返回源码而非执行结果、`Content-Type` 变成 `application/octet-stream`），
以及同目录下 200 与 404 的稳定分布。