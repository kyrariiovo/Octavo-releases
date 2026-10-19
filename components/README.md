# Octavo 文档转换组件

[下载组件 0.3.5 · Apple Silicon](https://github.com/kyrariiovo/Octavo-releases/releases/download/converters-0.3.5/Octavo-ConversionTools-0.3.5-AppleSilicon.dmg) · [更新说明](../notes/converters-0.3.5.md)

组件已并入 Octavo 统一发行仓库。仅支持 macOS Apple Silicon；Windows、Android 暂未提供解码和转换组件。

这里仅分发可选的开源转换工具、对应许可证和构建脚本，不包含 Octavo 阅读器应用或应用源码。PDF 阅读器的默认安装不需要这些工具。

组件目前适用于 Apple Silicon Mac。下载约 396 MiB，安装后独立占用约 1 GB。用户可在 Octavo 中首次打开非 PDF 文档时选择下载，或使用左下角“更多 → 下载文档转换组件…”；确认后才下载，文档始终留在本机。

## 包含工具

| 工具 | 作用 |
| --- | --- |
| LibreOffice 26.8.0 | DOC、DOCX、ODT、RTF 转 PDF |
| Tectonic 0.17.0、离线常用宏包与 Fandol 字体 | TEX 编译为 PDF |
| caj2pdf、PyMuPDF、JBIG／JBIG2 解码器 | 支持部分 CAJ、KDH 内部结构 |

来源、版本、许可证及必要修改见 [ThirdParty/README.md](ThirdParty/README.md)。资源许可文本位于 [Resources/ConverterLicenses](Resources/ConverterLicenses)。CAJ、KDH 兼容范围受上游限制；LaTeX 项目需保留图片、参考文献和模板，特殊宏包可能不受支持；缺失字体可能改变 Office 文档排版。

## 维护构建

在对应架构的 Mac 上，准备 Command Line Tools 和 Python 3.10+ 后执行：

```sh
./Scripts/prepare_converters.sh /path/to/python3
./Scripts/package_conversion_tools.sh
```

脚本从官方 LibreOffice／Tectonic 发布地址及 PyPI 获取依赖，并编译、冻结独立转换进程。准备后的二进制不提交到 Git，组件 DMG 通过 Releases 分发。

DMG 内只有 `Converters` 与 `ConverterLicenses`，不包含阅读器；应用下载后校验完整文件的 SHA-256，再安装到用户的 Application Support 目录。每次组件更新应使用新版本及新校验码，不覆盖已发布资源。
