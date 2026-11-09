"""工程单位换算器（Flet 1.x）

本地运行：
    flet run main.py

打包安卓 APK：
    flet build apk

换算原理：每个单位记录“1 个单位等于多少基准单位”的系数 rate，
换算时先乘 rate 归一到基准单位，再除以目标单位的 rate。
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

import flet as ft

APP_TITLE = "工程单位换算器"
AUTHOR = "康宝曾国祥 编写"


@dataclass(frozen=True)
class Unit:
    key: str  # 程序内部使用的唯一标识，和显示文字分开，改文案不影响逻辑
    label: str  # 显示给用户的名称，如 “英寸 in”
    rate: float | None = None  # 1 个该单位 = rate 个基准单位


@dataclass(frozen=True)
class Category:
    key: str
    label: str
    units: tuple[Unit, ...]
    is_temperature: bool = False  # 温度是“偏移量”换算，不能简单乘系数


CATEGORIES: tuple[Category, ...] = (
    Category(
        "length",
        "长度",
        (
            Unit("m", "米 m", 1.0),
            Unit("mm", "毫米 mm", 0.001),
            Unit("cm", "厘米 cm", 0.01),
            Unit("in", "英寸 in", 0.0254),
            Unit("ft", "英尺 ft", 0.3048),
        ),
    ),
    Category(
        "area",
        "面积",
        (
            Unit("m2", "平方米 m²", 1.0),
            Unit("mm2", "平方毫米 mm²", 1e-6),
            Unit("cm2", "平方厘米 cm²", 1e-4),
            Unit("in2", "平方英寸 in²", 0.00064516),
        ),
    ),
    Category(
        "mass",
        "质量（重量）",
        (
            Unit("kg", "千克 kg", 1.0),
            Unit("g", "克 g", 0.001),
            Unit("t", "吨 t", 1000.0),
            Unit("lb", "磅 lb", 0.45359237),
            Unit("oz", "盎司 oz", 0.028349523125),
        ),
    ),
    Category(
        "force",
        "力 / 拉力",
        (
            Unit("N", "牛顿 N", 1.0),
            Unit("kN", "千牛 kN", 1000.0),
            Unit("kgf", "公斤力 kgf", 9.80665),
            Unit("lbf", "磅力 lbf", 4.4482216152605),
        ),
    ),
    Category(
        "torque",
        "扭力（扭矩）",
        (
            Unit("Nm", "牛米 N·m", 1.0),
            Unit("kgfm", "公斤力米 kgf·m", 9.80665),
            Unit("lbfft", "磅力英尺 lbf·ft", 1.3558179483314004),
        ),
    ),
    Category(
        "temperature",
        "温度",
        (
            Unit("c", "摄氏度 ℃"),
            Unit("f", "华氏度 ℉"),
        ),
        is_temperature=True,
    ),
    Category(
        "heat",
        "热量 BTU",
        (
            Unit("btu", "BTU", 1.0),
            Unit("kj", "千焦 kJ", 0.9478171203133172),
            Unit("kcal", "千卡 kcal", 3.9683207193277963),
        ),
    ),
    Category(
        "flow",
        "气体流量",
        (
            Unit("m3h", "m³/h 立方米每小时", 1.0),
            Unit("lmin", "L/min 升每分钟", 0.06),
            Unit("cfm", "CFM 立方英尺每分钟", 1.69901079552),
        ),
    ),
    Category(
        "power",
        "电器功率",
        (
            Unit("w", "瓦 W", 1.0),
            Unit("kw", "千瓦 kW", 1000.0),
            Unit("ps", "公制马力 PS", 735.49875),
            Unit("hp", "英制马力 hp", 745.6998715822702),
            Unit("btuh", "BTU/h", 0.2930710701722222),
        ),
    ),
    Category(
        "pressure",
        "压强",
        (
            Unit("mpa", "兆帕 MPa", 1_000_000.0),
            Unit("bar", "巴 bar", 100_000.0),
            Unit("kpa", "千帕 kPa", 1_000.0),
            Unit("kgfcm2", "公斤力/平方厘米 kgf/cm²", 98066.5),
            Unit("psi", "磅/平方英寸 psi", 6894.757293168361),
        ),
    ),
)

CATEGORY_BY_KEY = {c.key: c for c in CATEGORIES}

# 允许的“输入中”形态：空、符号、半截小数、科学计数法（如 "1e"、"-"、"."）
_PARTIAL_NUMBER = re.compile(r"^[+-]?(\d+(\.\d*)?|\.\d+)?([eE][+-]?\d*)?$")


def convert(category: Category, from_key: str, value: float) -> dict[str, float]:
    """把 from_key 单位的 value 换算成该类别下其他所有单位。"""
    if category.is_temperature:
        if from_key == "c":
            return {"f": value * 9 / 5 + 32}
        return {"c": (value - 32) * 5 / 9}

    source = next(u for u in category.units if u.key == from_key)
    base = value * (source.rate or 0.0)
    return {
        unit.key: base / unit.rate
        for unit in category.units
        if unit.key != from_key and unit.rate
    }


def format_value(value: float) -> str:
    """把结果格式化成好读的字符串：去掉多余的 0，过大/过小用科学计数法。"""
    if not math.isfinite(value):
        return ""
    if value == 0:
        return "0"
    magnitude = abs(value)
    if magnitude >= 1e9 or magnitude < 1e-6:
        return f"{value:.6g}"
    # 固定 10 位小数再裁掉尾部的 0，可消除 25.400000000000002 这类浮点噪声
    text = f"{value:.10f}".rstrip("0").rstrip(".")
    return text or "0"


def main(page: ft.Page) -> None:
    page.title = APP_TITLE
    page.theme_mode = ft.ThemeMode.SYSTEM
    if page.web:
        # Web 版（iPhone PWA）没有系统的中文回退字体，不内置就会显示成方块
        page.fonts = {"NotoSansSC": "fonts/NotoSansSC-Regular.otf"}
        page.theme = ft.Theme(font_family="NotoSansSC")
    # Flet 1.x 里 scroll / padding 从 Page 移到了 View 上
    page.views[0].scroll = ft.ScrollMode.AUTO
    page.views[0].padding = ft.Padding.symmetric(horizontal=16, vertical=12)

    state: dict[str, Category] = {"category": CATEGORIES[0]}
    fields: dict[str, ft.TextField] = {}
    fields_box = ft.Column(spacing=10)

    def clear_all(_: ft.Event | None = None) -> None:
        for field in fields.values():
            field.value = ""
        page.update()

    def on_value_change(e: ft.Event[ft.TextField]) -> None:
        field = e.control
        key = field.data  # 在重建界面时把单位 key 挂在 data 上
        category = state["category"]
        text = (field.value or "").strip()

        if text == "":
            for other_key, other in fields.items():
                if other_key != key:
                    other.value = ""
            page.update()
            return

        # 正在输入 "-"、"1." 这类中间状态时先不换算，否则会打断输入
        if not _PARTIAL_NUMBER.match(text):
            return

        try:
            value = float(text)
        except ValueError:
            return
        if not math.isfinite(value):
            return

        for target_key, result in convert(category, key, value).items():
            fields[target_key].value = format_value(result)
        # 只更新其他输入框：当前输入框保持用户原样，避免光标跳动 / 小数被吃掉
        page.update()

    def rebuild(category_key: str) -> None:
        category = CATEGORY_BY_KEY.get(category_key)
        if category is None:
            return
        state["category"] = category
        fields.clear()
        fields_box.controls = []
        for unit in category.units:
            field = ft.TextField(
                label=unit.label,
                hint_text="输入数值",
                data=unit.key,
                on_change=on_value_change,
                border=ft.OutlineInputBorder(border_radius=10),
            )
            fields[unit.key] = field
            fields_box.controls.append(field)
        page.update()

    header = ft.Column(
        controls=[
            ft.Text(APP_TITLE, size=24, weight=ft.FontWeight.BOLD),
            ft.Text(AUTHOR, size=12, color=ft.Colors.GREY_600),
        ],
        spacing=2,
    )

    category_dropdown = ft.Dropdown(
        label="换算类别",
        value=CATEGORIES[0].key,
        options=[
            ft.DropdownOption(key=c.key, text=c.label) for c in CATEGORIES
        ],
        on_select=lambda e: rebuild(e.control.value),
        border=ft.OutlineInputBorder(border_radius=10),
    )

    page.add(
        header,
        category_dropdown,
        fields_box,
        ft.Row(
            controls=[
                ft.Text(
                    "在任意一栏输入数字，其他单位自动换算",
                    size=11,
                    color=ft.Colors.GREY_600,
                    expand=True,
                ),
                ft.TextButton("清空", icon=ft.Icons.CLEAR_ALL, on_click=clear_all),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
    rebuild(CATEGORIES[0].key)


if __name__ == "__main__":
    ft.run(main)
