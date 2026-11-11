# web-dirs 字典

## 来源

整理自 SecLists `Discovery/Web-Content/`（`common.txt`、`raft-small-directories.txt`、
`raft-medium-directories.txt`）与 dirsearch `db/dicc.txt`，按原始顺序合并、逐行 trim、
剔除注释行与空行、精确去重（保持大小写），截断至 30000 行。
未引入 Assetnote 与 OneListForAll 的超大合集，需要更大体量时按上游原文件自行替换。

## 适用方位

用于 Web 服务的目录与文件枚举：定位后台入口、接口前缀、中间件默认路径、
配置与版本库残留、备份压缩包命名。判据看 200/204 直接命中、301/302 跳转链与
`Location` 前缀、403 存在但禁读，以及相同路径下响应长度与 `Content-Length` 的基线差异；
对返回统一错误页的目标，用长度分布与相似度去噪后再判定。