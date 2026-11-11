# sensitive-files 字典

## 来源

以 SecLists `Discovery/Web-Content/quickhits.txt` 为基础（过滤掉纯目录型条目与注释），
补充版本库残留（`.git/HEAD`、`.svn/entries`）、环境与配置文件（`.env`、`web.config`、
`application.yml`、`appsettings.json`）、日志、数据库导出与备份包命名、私钥与证书文件，
剔除含 `%` 的 fuzz 标记行与纯目录条目后精确去重，共 2072 行。

## 适用方位

用于敏感文件与配置残留检查：验证源码与历史提交泄露（`.git` 可直接 dump 时还原全部代码）、
凭据泄露（`.env`、`config.php`、`.htpasswd`）、数据库与整站备份可下载、私钥泄露。
判据是 200 且响应内容出现特征串（`[core]`、`repositoryformatversion`、`DB_PASSWORD`、
`-----BEGIN`），403/302 只说明路径存在，需再看是否被鉴权或跳转到登录页。