独立的可选文档转换组件 **0.3.5 / Apple Silicon**。组件包中只有开源转换引擎与许可证，不包含 Octavo 阅读器或阅读器源码。

应用不会默认携带或下载这些资源。用户在首次打开需要转换的文档时确认下载，或从“更多 → 下载文档转换组件…”获取；完成校验后安装到用户的 Application Support 目录，不替换应用程序。

下载约 **396 MiB**，安装后约占 **1 GB**。本包包含 LibreOffice 26.8.0、Tectonic 0.17.0 与离线常用宏包／中文字体、caj2pdf、PyMuPDF、JBIG／JBIG2 解码器。DOC、DOCX、ODT、RTF 可转换为 PDF；TEX 需保留工程附属文件，特殊宏包可能不支持；CAJ／KDH 仅支持部分内部结构。缺失字体可能影响排版。

第三方许可证位于组件包的 `ConverterLicenses`，来源、必要修改与构建脚本见本仓库的 [components/](https://github.com/kyrariiovo/Octavo-releases/tree/main/components) 目录。工具仅在本机转换，文档不会上传。

```text
35a1ab2a8ef921b12bb21d21b5fc742b6a67b87ba166a7f9978484284404b378  Octavo-ConversionTools-0.3.5-AppleSilicon.dmg
```

统一下载入口：[Octavo-releases](https://github.com/kyrariiovo/Octavo-releases)。仅 macOS Apple Silicon 提供此可选组件，Windows、Android 暂未提供。
