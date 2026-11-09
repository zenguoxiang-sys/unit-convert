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

## 部署

推送到 `main` 分支后，GitHub Actions 会自动构建并发布到 GitHub Pages
（`.github/workflows/deploy-pages.yml`）。

第一次使用需要在仓库 **Settings → Pages → Build and deployment → Source**
选择 **GitHub Actions**。

## 打安卓 APK

仓库 **Actions → Build Android APK → Run workflow**，完成后在该次运行的
Artifacts 里下载 `unit-convert-apk`。
