# 工程单位换算器

用 Python + [Flet](https://flet.dev) 写的离线单位换算工具，支持：

长度、面积、质量、力、扭矩、温度、热量、气体流量、功率、压强，共 10 类。

## 手机直接用（PWA）

**https://zenguoxiang-sys.github.io/unit-convert/**

- iPhone：Safari 打开 → 「分享」→「添加到主屏幕」
- Android：Chrome 打开 → 菜单 →「添加到主屏幕」
- 也可以直接用浏览器打开，不装任何东西

## 本地运行

```bash
python3 -m pip install "flet==1.1.2"
flet run main.py
```

## 部署（GitHub Pages）

`docs/` 是**轻量网页版**（纯 HTML/JS，约 35 KB，秒开、可离线），用 Pages 的
**Deploy from a branch** 发布：

1. 仓库 **Settings → Pages → Build and deployment**
2. Source 选 **Deploy from a branch**
3. Branch 选 `main`，目录选 **`/docs`**，保存
4. 等 1 分钟，访问 https://zenguoxiang-sys.github.io/unit-convert/

网页版的数据来自 `main.py`，改完代码后重新生成：

```bash
python3 build_lite.py
cp web-lite/index.html docs/index.html
```

> 之前那套 Flutter/Pyodide 的网页版（45 MB，首屏慢）已不再使用；
> 源码和 APK 构建仍在 `.github/workflows/build-apk.yml`。

## 打安卓 APK

仓库 **Actions → Build Android APK → Run workflow**，完成后在该次运行的
Artifacts 里下载 `unit-convert-apk`。
