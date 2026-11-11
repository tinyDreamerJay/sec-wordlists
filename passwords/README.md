# passwords 字典

## 来源

SecLists `Passwords/Common-Credentials/10k-most-common.txt` 为前段，
后接 berzerk0/Probable-Wordlists `Top304Thousand-probable-v2.txt` 的按概率排序部分，
合并后转小写、不区分大小写去重，截断至 100000 行。未包含 rockyou 全量（体积大，按需另行下载）。

## 适用方位

用于口令类攻击的字典输入：在线喷洒与撞库（配合用户名或邮箱轮换）、离线爆破（hashcat/John 的 wordlist 模式）、
以及口令强度基线验证。判据是登录响应差异（状态码、跳转、`Set-Cookie`、错误文案长度）
或离线哈希比对命中；在线场景务必控制速率与账号锁定阈值。