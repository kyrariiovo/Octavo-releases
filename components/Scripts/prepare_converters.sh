#!/bin/zsh
set -euo pipefail
cd "${0:A:h:h}"
if (( $# > 1 )); then echo "用法：./Scripts/prepare_converters.sh [Python 3.10+ 可执行文件]" >&2; exit 2; fi
task_python="${1:-python3}"
"$task_python" Scripts/prepare_converters.py
