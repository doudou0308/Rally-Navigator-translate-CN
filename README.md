# Rally Navigator 简体中文汉化包 / Simplified Chinese Localization

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **English** | [**简体中文**](#rally-navigator-简体中文汉化包)

---

**Rally Navigator** is a professional rally roadbook creation software (Windows/macOS). This project provides a **Simplified Chinese translation** covering **99%+** of the application's UI text.

**Rally Navigator** 是一款专业的拉力赛路书制作软件（Windows/macOS）。本项目为其提供了**简体中文翻译**，覆盖了软件的 **99%+** 界面文本。

---

## 成果预览 / Preview

汉化覆盖软件全部核心界面 / Covers all core UI areas:

| Category | Examples |
|----------|---------|
| 菜单 / Menus | 文件、编辑、视图、帮助 / File, Edit, View, Help |
| 拉力术语 / Rally Terms | CAP、航点、路书、行程表、控制点 |
| 地形道路 / Terrain | 沙丘、岩石、涉水、柏油路、碎石 |
| 对话框 / Dialogs | 警告、确认、错误、保存、导出 |
| 设置 / Settings | Preferences, Language, Theme, Map |
| PDF 导出 / PDF Export | 路书 PDF、行程表、安全计划 |

- 总条目 / Total entries: **1,404**
- 已翻译 / Translated: **1,358 (96.7%)**
- 保留原文 / Kept as-is: **39** (品牌名/格式名 / brand names & formats)

---

## 快速开始 / Quick Start

### 前置条件 / Prerequisites

- 已安装 **Rally Navigator** / Installed Rally Navigator
- Python 3.7+

### 第一步：生成中文翻译 / Step 1: Generate translation

```bash
cd "Rally Navigator translate CN"
python translate.py
```

默认输出 / Default output: `resources/locales/zh-Hans-CN/translation.json`

### 第二步：部署到软件 / Step 2: Deploy

**方法 A（推荐 / Recommended）— 替换立陶宛语 / Replace Lithuanian**

```powershell
# 备份立陶宛语原文 / Backup Lithuanian original
Copy-Item "C:\Program Files\Rally Navigator\resources\locales\lt\translation.json" `
         "C:\Program Files\Rally Navigator\resources\locales\lt\translation.json.lt.bak"

# 部署中文翻译 / Deploy Chinese translation
Copy-Item ".\resources\locales\zh-Hans-CN\translation.json" `
         "C:\Program Files\Rally Navigator\resources\locales\lt\translation.json" -Force
```

**方法 B（自动化 / Automated）**

```powershell
# 修改 deploy.ps1 中的 $RallyPath 路径后执行
.\deploy.ps1
```

### 第三步：在软件中启用 / Step 3: Enable in the app

1. 启动 **Rally Navigator** / Launch the app
2. 打开菜单 / Open menu: **System and Menu Language**
3. 选择 / Select: **Lietuviškai** *(Lithuanian — 立陶宛语)*
4. 界面切换为简体中文 / Interface switches to Chinese

> **为什么选择立陶宛语？ / Why Lithuanian?**
>
> The app's language list is hardcoded inside `app.asar`. Adding a new language requires modifying and repacking the asar file, which is fragile. **Replacing an existing minority language** (Lithuanian) is simpler, more stable, and reversible.
>
> 该软件的语言列表硬编码在 `app.asar` 中。修改打包 asar 的方式不稳定。**替换现有小众语言（立陶宛语）** 是最简单、最稳定、可逆的方法。

---

## 项目结构 / Project Structure

```
Rally Navigator translate CN/
├── translate.py              # CLI 入口 / Entry point
├── deploy.ps1                # 一键部署脚本 / One-click deploy
├── src/
│   ├── translator.py         # 翻译核心逻辑 / Core logic
│   └── trans_map.py          # 翻译字典（1418 条） / Dictionary (1418 entries)
├── README.md                 # 双语文档 / Bilingual docs
├── .gitignore
└── LICENSE
```

---

## 自定义翻译 / Customization

编辑 / Edit `src/trans_map.py`：

```python
trans_map = {
    "Original English Text": "Your Translation",
}
```

然后重新运行 / Then re-run:

```bash
python translate.py
```

之后重新部署 / Then re-deploy (Step 2 above).

---

## 还原方法 / How to Restore

```powershell
Copy-Item "C:\Program Files\Rally Navigator\resources\locales\lt\translation.json.lt.bak" `
         "C:\Program Files\Rally Navigator\resources\locales\lt\translation.json" -Force
```

删除备份文件 / To also remove the backup:

```powershell
Remove-Item "C:\Program Files\Rally Navigator\resources\locales\lt\translation.json.lt.bak"
```

---

## 工作原理 / How It Works

```
en/translation.json  ──▶  translate.py  ──▶  zh-Hans-CN/translation.json
      (1,404 entries)       + trans_map            (Chinese translation)
                               (1,418 mappings)

zh-Hans-CN/translation.json  ──▶  Copy to lt/  ──▶  Select "Lietuviškai" in app
```

---

## 常见问题 / FAQ

**Q: 软件更新后失效怎么办？/ Lost after app update?**
A: 软件更新会覆盖 `resources/` 目录，重新执行部署步骤即可。App updates overwrite `resources/`. Just re-deploy.

**Q: 如何补充未翻译的条目？/ How to add missing translations?**
A: 运行 `python translate.py` 查看列表，将条目加入 `src/trans_map.py` 后重新生成。Run `python translate.py` to see the untranslated list, add entries to `src/trans_map.py`, then regenerate.

**Q: 为什么有些条目保留了英文？/ Why are some entries kept in English?**
A: 品牌名（Rally Navigator, RallySafe, TerraPirata 等）、文件格式（PDF, CSV, GPX, KML 等）和数字条目保持原文。Brand names, file format names, and numeric entries remain in English.

---

## License

MIT
