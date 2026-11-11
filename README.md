# sec-wordlists

分类整理的渗透测试字典集合：每个子目录一份纯文本词表 + 一份两节说明（来源 / 适用方位）。

| 子目录 | 一句话 | 数据取向 |
| --- | --- | --- |
| `web-dirs/` | Web 目录与文件枚举字典，找后台、接口前缀、残留文件与备份包。 | 国际基线（待国内化） |
| `subdomains/` | 子域名爆破字典，配合解析与证书反查扩面。 | 国际基线（待国内化） |
| `params/` | GET/POST 参数名字典，用于隐藏参数发现与越权、注入探测。 | 国际基线（待国内化） |
| `api-endpoints/` | API 路径与版本前缀字典，直打接口面。 | 国际基线（待国内化） |
| `passwords/` | 口令字典，段序即权重，国内 TOP1000 打头。 | **国内近年** |
| `usernames/` | 用户名字典，通用账号 + 真实手机号 + 姓名拼音。 | **国内近年** |
| `default-creds/` | 默认口令对，格式 `user:pass`，国内安全设备优先。 | **国内近年** |
| `sensitive-files/` | 敏感文件与配置残留路径，检查 .git/.env/备份/密钥泄露。 | 国际基线（待国内化） |
| `extensions/` | 文件后缀字典，用于后缀碰撞与上传、备份命名猜测。 | 国际基线（待国内化） |

## 来源取向

`passwords/`、`usernames/`、`default-creds/` 三份已按国内近年重做，上游是仍在维护的中文项目
（fuzzDicts、SaiDict、华为安全产品缺省口令速查表），段内顺序按国内实战命中率排，
`123456 / 5201314 / 1314520 / woaini` 在国内 TOP 段，`sangfor / leadsec / venus` 在国内设备段。
西方数据（Probable-Wordlists、SecLists 英文口令与用户名）降级为独立的
`passwords-intl.txt` / `usernames-intl.txt`，默认不加载。

其余六个子目录仍是国际基线（SecLists / dirsearch），特征是国内 CMS 路径（`/dede/`、`/phpmyadmin/`、
`/WEB-INF/web.xml`、`/actuator/env`）与国内子域命名（`app`、`m`、`api`、`open`、`oa`）覆盖不足，
按同样标准替换时需换成 fuzzDicts `directoryDicts/`、`subdomainDicts/` 与国内常见前缀表。

## 统一上游

- 国内：fuzzDicts <https://github.com/TheKingOfDuck/fuzzDicts>、SaiDict <https://github.com/Stardustsky/SaiDict>
- 国际：SecLists <https://github.com/danielmiessler/SecLists>、dirsearch <https://github.com/maurosoria/dirsearch>、
  Assetnote Wordlists <https://wordlists.assetnote.io>、Probable-Wordlists <https://github.com/berzerk0/Probable-Wordlists>、
  OneListForAll <https://github.com/six2dez/OneListForAll>

所有文件均为 UTF-8 无 BOM、LF、每行一条、已去重；来源与处理方式见各子目录 README，
构建脚本在 `tools/`。