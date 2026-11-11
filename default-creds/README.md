# default-creds 字典

## 来源

国内设备与中间件段在前（924 行，格式 `user:pass`）：

- **华为安全产品缺省用户名密码速查表**（`passwordDict/华为安全产品默认用户名密码速查表.xlsx`，
  文档版本 01，发布 2014-12-26）：从 Console/Telnet 列提取 `user/pass` 形态，得 18 条
  唯一口令对（`admin/Admin@123` 一类国内设备出厂默认，至今仍是实测高频）。
- **常见安全设备默认口令清单**（`passwordDict/常见安全设备默认口令清单.xlsx`）：逐行取
  「默认账号 × 默认密码」组合，覆盖深信服（sangfor）、网神/奇安信（leadsec）、启明（venus）、
  联想（lenovo）、科来（colasoft）、天融信等 68 条。
- **fuzzDicts `passwordDict/Middleware/`**：`tomcat-user/pass` 交叉、`weblogic.txt`、`zabbix.txt`、
  `axis.txt`（115 条）。
- **SaiDict `ServiceWeakPass/ftp弱口令/`**：`ftp-user`（8）× `ftp-pass`（176）交叉取前段 470 条。

国际基线保留 253 条（SecLists `Passwords/Default-Credentials/` 的 tomcat/ssh/mysql/ftp
betterdefaultpasslist + 常见 `admin:admin` 系），排在最后。

处理：xlsx 用 openpyxl 读取，单元格内多值按换行、`/`、`,`、`;`、`、` 切分后做笛卡尔组合；
剔除含空格、含中文、超长的条目；精确去重；UTF-8 无 BOM、LF。

## 适用方位

用于默认凭据尝试，优先打国内目标最常暴露的管理面：深信服 SSL VPN/AC/AF、网神/奇安信 WAF
与审计、启明 天玥/审计、华为 USG/Eudemon/AntiDDoS 的 Console 与 Web、以及 Tomcat Manager、
Weblogic 控制台、Zabbix、Axis2。判据是登录成功后出现的会话 Cookie、管理页标题、设备 banner
或版本回显；先用指纹（banner、favicon 哈希、登录页静态资源路径）确认厂商型号，
再只试对应厂商那几行，比全量盲试更省请求也更不容易触发锁定。