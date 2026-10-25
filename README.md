# Octavo这个用来看pdf

macOS、Windows、Android 原生 PDF 阅读、页面编辑和标记工具。

本仓库统一提供三个平台安装包、macOS 可选解码与转换组件、版本清单及更新说明。`components/` 仅保留开源转换工具的源码、构建脚本和许可证。

| 平台 | 当前版本 | 下载 | 更新说明 |
| --- | --- | --- | --- |
| macOS 13+ · Apple Silicon / Intel | 0.3.6 | [安装包](https://github.com/kyrariiovo/Octavo-releases/releases/download/macos-0.3.6/Octavo-macOS-0.3.6-Universal.dmg) | [查看说明](notes/macos-0.3.6.md) |
| Windows 10 2004+ · x64 | 0.5.9 | [安装包](https://github.com/kyrariiovo/Octavo-releases/releases/download/windows-0.5.9/Octavo-Setup-0.5.9-x64.exe) | [查看说明](notes/windows-0.5.9.md) |
| Android 8.0+ | 0.10.0 | [安装包](https://github.com/kyrariiovo/Octavo-releases/releases/download/android-0.10.0/Octavo-Android-0.10.0.apk) | [查看说明](notes/android-0.10.0.md) |

## macOS 可选解码与转换组件

[下载组件 0.3.5 · Apple Silicon](https://github.com/kyrariiovo/Octavo-releases/releases/download/converters-0.3.5/Octavo-ConversionTools-0.3.5-AppleSilicon.dmg) · [更新说明](notes/converters-0.3.5.md) · [组件来源与许可证](components/README.md)

支持 Word 文档、LaTeX 和部分 CAJ／KDH 的本机转换，包含 JBIG／JBIG2 解码器。下载约 396 MiB，安装后约占 1 GB；在 macOS 软件“更多 → 下载文档转换组件…”中按需安装。当前仅支持 Apple Silicon，Windows、Android 暂未提供此功能。

SHA-256：`35a1ab2a8ef921b12bb21d21b5fc742b6a67b87ba166a7f9978484284404b378`。组件版本独立于阅读器版本；无需为了安装组件重新安装阅读器。

## 软件内更新

首次需要安装上述版本。之后默认每天自动检查，发现新版后在合适时机弹窗提醒，也可以手动检查或关闭自动检查。

- macOS：顶部软件菜单或“更多 → 检查更新…”。安装前询问保存 PDF，完成后重新打开应用。
- Windows：“更多 → 检查更新…”。安装前询问保存 PDF，系统可能要求管理员确认。
- Android：主页“更多 → 软件更新…”或阅读界面“更多 → 软件更新…”。下载后需要系统确认安装，首次可能需要允许安装软件。

更新检查只请求版本信息和安装包，不上传 PDF、谱库、标记或阅读记录。更新包在安装前经过签名及完整性校验。

## 安装说明

macOS：打开 DMG，将应用拖入“应用程序”。当前尚无 Developer ID 签名及 Apple 公证，系统可能要求在“隐私与安全性”中确认打开。

Windows：运行 EXE 安装器，可选择安装位置。自带运行环境；当前安装器尚无 Authenticode 发行签名，系统可能显示信誉提示。

Android：直接安装 APK，沿用原有签名证书，可覆盖升级并保留数据。

应用闭源发行；所用第三方组件的版权和许可证按各自要求保留。
