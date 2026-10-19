# 文档转换工具来源

转换工具通过独立后台进程运行，不作为 PDF 阅读器的链接库。用户文档保留在本机。默认阅读器不附带这些资源；首次需要时经用户确认才下载，或从“更多”主动下载，安装到用户的 Application Support 目录。

当前 Apple Silicon 可选组件通过本仓库 Releases 分发，DMG 中只有 `Converters` 与 `ConverterLicenses`。组件不包含阅读器，不会替换应用程序；只有校验及资源完整性检查成功后才启用。固定 SHA-256 随 Release 公布。

维护资源可由 `Scripts/prepare_converters.sh` 准备，位于被 Git 忽略的 `Resources/Converters/`，仅供转换测试和组件维护使用。

- LibreOffice 26.8.0：<https://www.libreoffice.org/>，官方 macOS 应用；原始应用包内保留完整许可证和资源。
- Tectonic 0.17.0：<https://github.com/tectonic-typesetting/tectonic/releases/tag/tectonic%400.17.0>，MIT 许可证。TeX 资源来自其默认开源 TeX Live 资源包；按 `Scripts/latex-support.tex` 预取常用宏包、Fandol 中文字体和排版资源，离线 ZIP 内保留原始文件。TeX 宏包的版权、许可证及更新说明在对应源文件中；LPPL/GPL 许可文本一并随应用附带。
- caj2pdf：<https://github.com/caj2pdf/caj2pdf/tree/6c4bc32b15ce748d211f45d536f5d5511ef9f368>，GLWTPL。`caj2pdf/` 保存转换所需源码；本项目将 JBIG 动态库定位改为模块目录，并修正小于 4096 字节文件的反向查找。`pdfwutils.py` 遵循其文件头声明的 GPL-3.0-or-later，JBIG 包装遵循 FreeType 许可证。
- jbig2dec 0.20：<https://github.com/ArtifexSoftware/jbig2dec/tree/1d1347e38a55e657dcc4c8f1c77bb3a26bfc9ff3>，AGPL-3.0；`jbig2dec/` 保留编译所需源文件及许可文本。
- PyMuPDF 1.27.2：<https://github.com/pymupdf/PyMuPDF/tree/1.27.2>，使用 AGPL-3.0 开源版本，作为 CAJ 转换进程里的 MuPDF 修复引擎。
- PyPDF2 2.2.0、Pillow 12.1.0、imagesize 1.3.0：使用各自开源许可证。`Scripts/collect_converter_licenses.py` 从构建环境的分发元数据收集许可，放入 `Resources/ConverterLicenses/`。
- PyInstaller 6.19.0：用于生成不依赖用户 Python 安装的独立工具，其 bootloader 遵循 GPL 及分发例外。
- Python 3.12：冻结到 CAJ worker 中，附带 PSF 及运行时第三方许可通知。Fandol 中文字体遵循 GPL-3.0 和字体嵌入例外，保留原始 README 和 COPYING。

CAJ/HN/C8/KDH 转换沿用上游可支持的结构，不能承诺所有知网格式均可转换；无法转换时保留原文件并显示导出 PDF 的指引。
