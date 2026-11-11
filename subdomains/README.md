# subdomains 字典

## 来源

整理自 SecLists `Discovery/DNS/` 的 `subdomains-top1million-5000.txt`、
`subdomains-top1million-110000.txt` 与 `dns-Jhaddix.txt`，全部转小写、
按不区分大小写去重、剔除空行，截断至 80000 行（前两万行来自 Jhaddix 的实战高频组合）。
保留一级标签形态（如 `dev-api`），不带通配符与占位符。

## 适用方位

用于子域名爆破与资产扩面：打主域下的开发/测试/内网跳板/管理后台/对象存储与 CDN 回源域名。
判据先看 DNS 解析是否命中，再过滤泛解析（随机标签探测对比响应），
对命中的 A/CNAME 记录做归属判断，最后用 HTTP 状态码、标题、证书 SAN 与 favicon 哈希确认是否同一资产。