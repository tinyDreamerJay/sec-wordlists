# sec-wordlists

分类整理的渗透测试字典集合：每个子目录一份纯文本词表 + 一份两节说明（来源 / 适用方位）。

| 子目录 | 一句话 |
| --- | --- |
| `web-dirs/` | Web 目录与文件枚举字典，找后台、接口前缀、残留文件与备份包。 |
| `subdomains/` | 子域名爆破字典，配合解析与证书反查扩面。 |
| `params/` | GET/POST 参数名字典，用于隐藏参数发现与越权、注入探测。 |
| `api-endpoints/` | API 路径与版本前缀字典，直打接口面。 |
| `passwords/` | 口令字典，按频次排序，用于在线喷洒与离线爆破。 |
| `usernames/` | 用户名字典，用于账号枚举与撞库组合。 |
| `default-creds/` | 默认口令对，格式 `user:pass`。 |
| `sensitive-files/` | 敏感文件与配置残留路径，检查 .git/.env/备份/密钥泄露。 |
| `extensions/` | 文件后缀字典，用于后缀碰撞与上传、备份命名猜测。 |

## 统一上游

- SecLists：<https://github.com/danielmiessler/SecLists>
- dirsearch：<https://github.com/maurosoria/dirsearch>
- Assetnote Wordlists：<https://wordlists.assetnote.io>
- Probable-Wordlists：<https://github.com/berzerk0/Probable-Wordlists>
- OneListForAll（聚合版）：<https://github.com/six2dez/OneListForAll>

所有文件均为 UTF-8 无 BOM、每行一条、已去重；来源与处理方式见各子目录 README。