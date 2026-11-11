# -*- coding: utf-8 -*-
"""构建国内优先的 passwords / usernames / default-creds 三份字典。

用法：
    python tools/build_cn_dicts.py <源文件目录>

<源文件目录> 需预先放好上游原件（fuzzDicts / SaiDict，含 GB18030 编码的原始文件）：
    pw_top1000.txt pw_top3000.txt pw_top19576.txt pw_group.txt pw_sai.txt
    pw_webshell.txt pw_birth.txt
    un_top500.txt un_sai_name.txt un_cnname.txt un_fuzz_user.txt
    un_sai_phone.txt un_phone.txt un_china.txt un_lastname.txt
    mw_tomcat-user.txt mw_tomcat-pass.txt mw_weblogic.txt mw_zabbix.txt mw_axis.txt
    wp_sai_ftp_ftp-user.txt wp_sai_ftp_ftp-pass.txt
    xlsx_*.xlsx（华为安全产品缺省口令速查表、常见安全设备默认口令清单）

输出：<仓库>/{passwords,usernames,default-creds}/*.txt，UTF-8 无 BOM + LF，段序即权重。
"""
import os
import re
import sys
import glob
import json
import openpyxl

TMP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.getcwd(), "_src")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
stats = {}

def read_lines(name, enc="utf-8"):
    path = os.path.join(TMP, name)
    with open(path, "r", encoding=enc, errors="replace", newline="") as f:
        return [ln.strip("\r\n") for ln in f]

def write_lines(path, lines):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for ln in lines:
            f.write(ln + "\n")

BAD_WS = re.compile(r"[\s\u3000]")
CJK = re.compile(r"[\u4e00-\u9fff]")

def add(seq, seen, line, lo=1, hi=64, allow_cjk=False):
    t = line.strip()
    if not t or t.startswith("#"):
        return
    if BAD_WS.search(t):
        return
    if not (lo <= len(t) <= hi):
        return
    if not allow_cjk and CJK.search(t):
        return
    if t in seen:
        return
    seen.add(t)
    seq.append(t)

# ---------------- passwords ----------------
pw = []
seen = set()
seg = {}
for tag, name, enc in [
    ("cn_top1000", "pw_top1000.txt", "utf-8"),
    ("cn_top3000", "pw_top3000.txt", "utf-8"),
    ("cn_top19576", "pw_top19576.txt", "utf-8"),
    ("cn_group_dict", "pw_group.txt", "gb18030"),
    ("cn_saidict_pass", "pw_sai.txt", "gb18030"),
    ("cn_webshell_pass", "pw_webshell.txt", "gb18030"),
    ("cn_birthday", "pw_birth.txt", "utf-8"),
]:
    before = len(pw)
    for ln in read_lines(name, enc):
        add(pw, seen, ln, lo=4, hi=64)
    seg[tag] = len(pw) - before

stats["passwords_segments"] = seg
stats["passwords_total"] = len(pw)
write_lines(os.path.join(ROOT, "passwords", "passwords.txt"), pw)

# ---------------- usernames ----------------
un = []
seen = set()
def add_user(seq, seen, line, lo=2, hi=40):
    t = line.strip()
    if not t or t.startswith("#"):
        return
    if BAD_WS.search(t) or CJK.search(t):
        return
    if re.search(r"['\"`;()<>|\\/=+*$#@!,%&]", t):
        return
    if not (lo <= len(t) <= hi):
        return
    if not re.fullmatch(r"[A-Za-z0-9._-]+", t):
        return
    if t in seen:
        return
    seen.add(t)
    seq.append(t)

seg_u = {}
for tag, name, cap in [
    ("cn_common_top500", "un_top500.txt", 0),
    ("cn_real_names", "un_sai_name.txt", 0),
    ("cn_name_abbr", "un_cnname.txt", 0),
    ("cn_user_base", "un_fuzz_user.txt", 0),
    ("cn_mobile_leaked", "un_sai_phone.txt", 60000),
    ("cn_mobile_pattern", "un_phone.txt", 0),
    ("cn_surname", "un_lastname.txt", 0),
]:
    before = len(un)
    lines = read_lines(name, "utf-8")
    if cap:
        lines = lines[:cap]
    for ln in lines:
        add_user(un, seen, ln)
    seg_u[tag] = len(un) - before

stats["usernames_segments"] = seg_u

# cn_pinyin_full: un_china.txt 是按字母序穷举生成的，直接用前 N 行会全落在 l 开头的姓上；
# 这里按“百家姓频次表”顺序做轮询取样，让 li/wang/zhang/liu/chen 等常见姓各占一份。
before = len(un)
pinyin_all = [x.strip() for x in read_lines("un_china.txt") if x.strip()]
surname_order = [x.strip() for x in read_lines("un_lastname.txt") if x.strip()]
surname_by_len = sorted(surname_order, key=len, reverse=True)  # 最长前缀优先，避免 li 吃掉 lin/liu/liang
per_surname = {s: [] for s in surname_order}
for name in pinyin_all:
    for s in surname_by_len:
        if name.startswith(s):
            per_surname[s].append(name)
            break
i = 0
while len(un) - before < 60000:
    added = False
    for s in surname_order:
        if i < len(per_surname[s]) and len(un) - before < 60000:
            add_user(un, seen, per_surname[s][i])
            added = True
    if not added:
        break
    i += 1
seg_u["cn_pinyin_full_by_surname"] = len(un) - before

stats["usernames_segments"] = seg_u
stats["usernames_total"] = len(un)
write_lines(os.path.join(ROOT, "usernames", "usernames.txt"), un)

# ---------------- default-creds ----------------
dc = []
seen = set()
seg_d = {}

def add_cred(user, pwd):
    u, p = str(user).strip(), str(pwd).strip()
    if not u or not p or len(u) > 40 or len(p) > 64:
        return
    if BAD_WS.search(u) or BAD_WS.search(p) or CJK.search(u) or CJK.search(p):
        return
    line = u + ":" + p
    if line in seen:
        return
    seen.add(line)
    dc.append(line)

def split_tokens(v):
    if v is None:
        return []
    s = str(v).replace("\u2002", " ").replace("\u3000", " ").replace("\xa0", " ")
    out = []
    for p in re.split(r"[\n\r/,;；、]+", s):
        p = p.strip()
        if p and p not in out:
            out.append(p)
    return out

# 1) 国内安全设备缺省口令（深信服等厂商清单 xlsx：设备|账号|密码）
vendor_rows = 0
for path in glob.glob(os.path.join(TMP, "xlsx_*.xlsx")):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    for ws in wb.worksheets:
        if ws.max_column < 3 or ws.max_row > 400:
            continue
        header = None
        for row in ws.iter_rows(values_only=True):
            cells = ["" if c is None else str(c) for c in row]
            if header is None:
                joined = "".join(cells)
                if ("账号" in joined or "用户名" in joined) and "密码" in joined and "BootROM" not in joined:
                    header = cells
                continue
            if not any(c.strip() for c in cells):
                continue
            users = split_tokens(cells[1]) if len(cells) > 1 else []
            pwds = split_tokens(cells[2]) if len(cells) > 2 else []
            for u in users:
                for p in pwds:
                    add_cred(u, p)
                    vendor_rows += 1
    wb.close()
seg_d["cn_vendor_device"] = len(dc)

# 2) 华为安全产品缺省口令（user/pass 单元格形态）
hw = 0
for path in glob.glob(os.path.join(TMP, "xlsx_*.xlsx")):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    for ws in wb.worksheets:
        for row in ws.iter_rows(values_only=True):
            for c in row:
                if c is None:
                    continue
                for m in re.finditer(r"([A-Za-z][A-Za-z0-9_.\-]{1,20})/([A-Za-z0-9@#$%^&*!_.\-]{2,32})", str(c)):
                    add_cred(m.group(1), m.group(2))
                    hw += 1
    wb.close()
seg_d["cn_huawei_device"] = len(dc) - seg_d.get("cn_vendor_device", 0)

# 3) 中间件/监控默认口令（fuzzDicts Middleware，本身是 user/pass 或 user、pass 分列）
for name in ("mw_weblogic.txt", "mw_zabbix.txt", "mw_axis.txt"):
    for ln in read_lines(name):
        if "/" in ln:
            u, p = ln.split("/", 1)
            add_cred(u, p)
tu = [x for x in read_lines("mw_tomcat-user.txt")]
tp = [x for x in read_lines("mw_tomcat-pass.txt")]
for u in tu:
    for p in tp:
        add_cred(u, p)
seg_d["cn_middleware"] = len(dc) - sum(seg_d.values())

# 4) FTP 弱口令（SaiDict ftp弱口令：user/pass 分列，交叉）
fu = read_lines("wp_sai_ftp_ftp-user.txt")
fp = read_lines("wp_sai_ftp_ftp-pass.txt")
for u in fu[:12]:
    for p in fp[:60]:
        add_cred(u, p)
seg_d["cn_ftp_weak"] = len(dc) - sum(seg_d.values())

# 5) 原国际基线（SecLists betterdefaultpasslist 合并结果，已入库）
base = os.path.join(ROOT, "default-creds", "default-creds.txt")
if os.path.exists(base):
    for ln in read_lines(os.path.abspath(base)):
        if ":" in ln:
            u, p = ln.split(":", 1)
            add_cred(u, p)
seg_d["intl_baseline"] = len(dc) - sum(v for k, v in seg_d.items() if k != "intl_baseline")

stats["default_creds_segments"] = seg_d
stats["default_creds_total"] = len(dc)
write_lines(os.path.join(ROOT, "default-creds", "default-creds.txt"), dc)

# ---------------- 热度截取：前 100 / 前 1000 ----------------
# 主文件段序即权重，所以直接取头部 N 行就是“按热度”的前 N 位。
tops = {}
for src, sub, stem, seq in (
    ("passwords", "passwords", "passwords", pw),
    ("usernames", "usernames", "usernames", un),
):
    for n in (100, 1000):
        if len(seq) >= n:
            out = os.path.join(ROOT, sub, "%s-top%d.txt" % (stem, n))
            write_lines(out, seq[:n])
            tops["%s-top%d" % (stem, n)] = n

stats["top_files"] = tops
print(json.dumps(stats, ensure_ascii=False, indent=2))
