#!/usr/bin/env python3
"""给 `flet build web` 生成的 index.html 打补丁。

Flutter 的模板只加了 `mobile-web-app-capable`（Chrome 用），Safari 认的是
`apple-mobile-web-app-capable`。补上它，iPhone 上“添加到主屏幕”后才会
全屏运行（不显示 Safari 地址栏）。
"""

import sys
from pathlib import Path

INDEX = Path("build/web/index.html")
META = '<meta name="apple-mobile-web-app-capable" content="yes">'


def main() -> int:
    if not INDEX.exists():
        print(f"找不到 {INDEX}，先执行 flet build web")
        return 1

    html = INDEX.read_text(encoding="utf-8")
    if META in html:
        print("index.html 已包含 apple-mobile-web-app-capable，跳过")
        return 0

    anchor = '<meta name="mobile-web-app-capable" content="yes">'
    if anchor not in html:
        print("找不到插入位置，index.html 结构可能变了")
        return 1

    html = html.replace(anchor, anchor + "\n  " + META)
    INDEX.write_text(html, encoding="utf-8")
    print("已补上 apple-mobile-web-app-capable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
