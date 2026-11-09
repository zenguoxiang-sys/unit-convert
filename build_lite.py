"""从 main.py 的 CATEGORIES 生成轻量网页版 index.html。

网页版是纯 HTML/CSS/JS（约 100 KB），不依赖 Flutter / Pyodide，
秒开、可离线；数据仍然以 main.py 为唯一来源，避免两套数据不一致。
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import main  # noqa: E402


def build_data() -> list[dict]:
    return [
        {
            "key": c.key,
            "label": c.label,
            "temp": c.is_temperature,
            "units": [
                {"key": u.key, "label": u.label, "rate": u.rate}
                for u in c.units
            ],
        }
        for c in main.CATEGORIES
    ]


def main_() -> int:
    template = (HERE / "web-lite" / "template.html").read_text(encoding="utf-8")
    data = json.dumps(build_data(), ensure_ascii=False, separators=(",", ":"))
    html = template.replace("__DATA__", data)
    out = HERE / "web-lite" / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"写入 {out}（{out.stat().st_size / 1024:.1f} KB）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main_())
