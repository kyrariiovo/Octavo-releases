#!/bin/zsh
set -euo pipefail
cd "${0:A:h:h}"
task_output_directory="${1:-$PWD/work/component-distribution}"
task_version="0.3.5"
task_architecture="$(uname -m)"
case "$task_architecture" in
    arm64) task_variant="AppleSilicon" ;;
    x86_64) task_variant="Intel" ;;
    *) echo "不支持的架构：$task_architecture" >&2; exit 1 ;;
esac
task_name="Octavo-ConversionTools-$task_version-$task_variant.dmg"
mkdir -p "$task_output_directory"
if [[ -e "$task_output_directory/$task_name" ]]; then
    echo "组件包已存在，未覆盖：$task_output_directory/$task_name" >&2
    exit 1
fi
task_stage="$(mktemp -d "${TMPDIR:-/tmp}/Octavo-tools-package.XXXXXX")"
trap 'rm -rf "$task_stage"' EXIT
for task_tool in LibreOffice.app/Contents/MacOS/soffice tectonic caj-worker/caj-worker; do
    [[ -x "Resources/Converters/$task_architecture/$task_tool" ]] || { echo "缺少转换工具：$task_tool" >&2; exit 1; }
done
mkdir -p "$task_stage/contents/Converters"
ditto "Resources/Converters/$task_architecture" "$task_stage/contents/Converters/$task_architecture"
cp Resources/Converters/latex-bundle.zip "$task_stage/contents/Converters/latex-bundle.zip"
ditto Resources/ConverterLicenses "$task_stage/contents/ConverterLicenses"
hdiutil create -volname "Octavo Conversion Tools $task_version" -srcfolder "$task_stage/contents" -fs HFS+ -format UDZO "$task_stage/$task_name"
hdiutil verify "$task_stage/$task_name"
mv "$task_stage/$task_name" "$task_output_directory/$task_name"
shasum -a 256 "$task_output_directory/$task_name"
