import flet as ft

def main(page: ft.Page):
    page.title = "工程单位换算器"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 16

    data = [
        {
            "cat": "长度",
            "items": [
                {"name": "米 m", "rate": 1},
                {"name": "毫米 mm", "rate": 0.001},
                {"name": "厘米 cm", "rate": 0.01},
                {"name": "英寸 in", "rate": 0.0254},
                {"name": "英尺 ft", "rate": 0.3048},
            ]
        },
        {
            "cat": "面积",
            "items": [
                {"name": "平方米 m²", "rate": 1},
                {"name": "平方毫米 mm²", "rate": 1e-6},
                {"name": "平方厘米 cm²", "rate": 1e-4},
                {"name": "平方英寸 in²", "rate": 0.00064516},
            ]
        },
        {
            "cat": "质量(重量)",
            "items": [
                {"name": "千克 kg", "rate": 1},
                {"name": "克 g", "rate": 0.001},
                {"name": "吨 t", "rate": 1000},
                {"name": "磅 lb", "rate": 0.45359237},
                {"name": "盎司 oz", "rate": 0.0283495},
            ]
        },
        {
            "cat": "力 / 拉力",
            "items": [
                {"name": "牛顿 N", "rate": 1},
                {"name": "千牛 kN", "rate": 1000},
                {"name": "公斤力 kgf", "rate": 9.80665},
                {"name": "磅力 lbf", "rate": 4.44822},
            ]
        },
        {
            "cat": "扭力(扭矩)",
            "items": [
                {"name": "牛米 N·m", "rate": 1},
                {"name": "公斤力米 kgf·m", "rate": 9.80665},
                {"name": "磅力英尺 lbf·ft", "rate": 1.35582},
            ]
        },
        {
            "cat": "温度",
            "is_temp": True,
            "items": [
                {"name": "摄氏度 ℃"},
                {"name": "华氏度 ℉"},
            ]
        },
        {
            "cat": "热量 BTU",
            "items": [
                {"name": "BTU", "rate": 1},
                {"name": "千焦 kJ", "rate": 0.947817},
                {"name": "千卡 kcal", "rate": 3.96832},
            ]
        },
        {
            "cat": "气体流量",
            "items": [
                {"name": "m³/h 立方米每小时", "rate": 1},
                {"name": "L/min 升每分钟", "rate": 0.06},
                {"name": "CFM 立方英尺每分钟", "rate": 1.69901},
            ]
        },
        {
            "cat": "电器功率",
            "items": [
                {"name": "瓦 W", "rate": 1},
                {"name": "千瓦 kW", "rate": 1000},
                {"name": "公制马力 PS", "rate": 735.49875},
                {"name": "英制马力 hp", "rate": 745.69987},
                {"name": "BTU/h", "rate": 0.293071},
            ]
        },
        {
            "cat": "压强",
            "items": [
                {"name": "兆帕 MPa", "rate": 1000000},
                {"name": "巴 bar", "rate": 100000},
                {"name": "千帕 kPa", "rate": 1000},
                {"name": "公斤力/平方厘米 kgf/cm²", "rate": 98066.5},
                {"name": "磅/平方英寸 psi", "rate": 6894.75729},
            ]
        }
    ]

    current_cat = None
    input_map = {}

    cat_select = ft.Dropdown(
        label="选择换算类别",
        options=[ft.DropdownOption(c["cat"]) for c in data],
        value=data[0]["cat"],
        on_change=lambda e: render()
    )
    container = ft.Column()

    def calc(src):
        val = src.value.strip()
        if not val:
            for i in input_map.values():
                i.value = ""
            page.update()
            return
        try:
            num = float(val)
        except ValueError:
            return
        if current_cat.get("is_temp"):
            if src.label == "摄氏度 ℃":
                f = num * 1.8 + 32
                input_map["华氏度 ℉"].value = f"{f:.4f}"
            else:
                c = (num - 32) / 1.8
                input_map["摄氏度 ℃"].value = f"{c:.4f}"
        else:
            src_rate = next(it["rate"] for it in current_cat["items"] if it["name"] == src.label)
            base = num * src_rate
            for item in current_cat["items"]:
                r = item["rate"]
                input_map[item["name"]].value = f"{base / r:.4f}"
        page.update()

    def render():
        nonlocal current_cat
        current_cat = next(c for c in data if c["cat"] == cat_select.value)
        container.controls.clear()
        input_map.clear()
        for item in current_cat["items"]:
            tf = ft.TextField(label=item["name"], on_change=lambda e,t=calc: t(e.control))
            input_map[item["name"]] = tf
            container.controls.append(tf)
        page.update()

    page.add(
        ft.Text("工程单位换算器", size=22, weight=ft.FontWeight.BOLD),
        ft.Text("康宝曾国祥编写", size=14, color=ft.colors.GREY_600),
        cat_select,
        container
    )
    render()

# 打包APK时不要加view参数！
ft.app(target=main)
