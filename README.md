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

网站就是 `docs/` 目录里的静态文件，用 Pages 的 **Deploy from a branch** 发布：

1. 仓库 **Settings → Pages → Build and deployment**
2. Source 选 **Deploy from a branch**
3. Branch 选 `main`，目录选 **`/docs`**，保存
4. 等 1 分钟，访问 https://zenguoxiang-sys.github.io/unit-convert/

重新生成静态文件（在本地）：

```bash
flet build web --yes --no-cdn --base-url /unit-convert/
python3 patch_web.py
rm -rf docs && cp -R build/web docs && touch docs/.nojekyll
```

> `.github/workflows/deploy-pages.yml` 是另一种方案（Actions 构建后发布），
> 需要手动触发，并确保 Pages 的 Source 选 **GitHub Actions**。

## 打安卓 APK

仓库 **Actions → Build Android APK → Run workflow**，完成后在该次运行的
Artifacts 里下载 `unit-convert-apk`。
