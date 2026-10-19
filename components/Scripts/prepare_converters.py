"""Rebuild the native-architecture, offline conversion resources from open sources.

Downloads official LibreOffice/Tectonic releases; Python packages come from PyPI.
No application is installed globally. Runtime tools are embedded under Resources.
"""
import hashlib
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import venv
import zipfile
from pathlib import Path

project = Path(__file__).resolve().parents[1]
os.chdir(project)
if sys.version_info < (3, 10):
    raise SystemExit("Preparing converters requires Python 3.10 or later; the installed app does not require Python.")
architecture = platform.machine()
if architecture not in ("arm64", "x86_64"):
    raise SystemExit("Prepare the resources on an arm64 or x86_64 Mac.")
work = project / "work/converter-preparation"
work.mkdir(parents=True, exist_ok=True)
root = project / "Resources/Converters"
tools = root / architecture
tools.mkdir(parents=True, exist_ok=True)


def run(*arguments, **kwargs):
    subprocess.run([str(a) for a in arguments], check=True, **kwargs)


def fetch(url, path, digest=None):
    path = Path(path)
    if not path.is_file():
        temporary = path.with_suffix(path.suffix + ".download")
        run("curl", "-fL", "--retry", "2", "--connect-timeout", "30", url, "-o", temporary)
        temporary.replace(path)
    if digest and hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise RuntimeError("Download checksum mismatch: " + str(path))
    return path


office_arch = "aarch64" if architecture == "arm64" else "x86_64"
office_url = f"https://download.documentfoundation.org/libreoffice/stable/26.8.0/mac/{office_arch}/LibreOffice_26.8.0_MacOS_{office_arch}.dmg"
office = tools / "LibreOffice.app"
if not office.is_dir():
    expected = "8858d8058da4f862f47559486814e65efc27294da67c5e4bb56b006b1ee59f89" if architecture == "arm64" else None
    image = fetch(office_url, work / f"libreoffice-{architecture}.dmg", expected)
    with tempfile.TemporaryDirectory(prefix="Octavo-office-") as mount:
        run("hdiutil", "attach", "-readonly", "-nobrowse", "-mountpoint", mount, image)
        try:
            run("ditto", Path(mount)/"LibreOffice.app", office)
        finally:
            run("hdiutil", "detach", mount)
tectonic_arch = "aarch64" if architecture == "arm64" else "x86_64"
archive_name = f"tectonic-0.17.0-{tectonic_arch}-apple-darwin.tar.gz"
tectonic = tools / "tectonic"
if not tectonic.is_file():
    expected = "a3f1cac7c5678f01661a92212f58480ae3b0634115d880dbc59e2953ded45667" if architecture == "arm64" else None
    archive = fetch(f"https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.17.0/{archive_name}", work/archive_name, expected)
    with tarfile.open(archive) as tar:
        binary = next(member for member in tar.getmembers() if member.name.split("/")[-1] == "tectonic" and member.isfile())
        tectonic.write_bytes(tar.extractfile(binary).read())
    tectonic.chmod(0o755)

environment = work / "python"
if not (environment/"bin/python").exists():
    venv.create(environment, with_pip=True)
python = environment/"bin/python"
run(python, "-m", "pip", "install", "--disable-pip-version-check", "-r", "Scripts/converter-requirements.txt")
run(python, "Scripts/collect_converter_licenses.py")
run("xcrun", "clang++", "-dynamiclib", "-std=c++11", "-arch", architecture, "-mmacosx-version-min=13.0", "ThirdParty/caj2pdf/lib/jbigdec.cc", "ThirdParty/caj2pdf/lib/JBigDecode.cc", "-o", work/"libjbigdec.so")
names = "jbig2 jbig2_arith jbig2_arith_int jbig2_arith_iaid jbig2_huffman jbig2_hufftab jbig2_segment jbig2_page jbig2_symbol_dict jbig2_text jbig2_generic jbig2_refinement jbig2_mmr jbig2_halftone jbig2_image".split()
objects = []
for name in names:
    output = work/(name+".o")
    run("xcrun", "clang", "-fPIC", "-arch", architecture, "-mmacosx-version-min=13.0", "-I", "ThirdParty/jbig2dec", "-c", "ThirdParty/jbig2dec/"+name+".c", "-o", output)
    objects.append(output)
run("xcrun", "clang++", "-dynamiclib", "-arch", architecture, "-mmacosx-version-min=13.0", "-I", "ThirdParty/jbig2dec", "ThirdParty/caj2pdf/lib/decode_jbig2data_x.cc", *objects, "-o", work/"libjbig2codec.so")
run(python, "-m", "PyInstaller", "--noconfirm", "--clean", "--onedir", "--name", "caj-worker", "--distpath", work/"dist", "--workpath", work/"build", "--specpath", work, "--paths", project/"ThirdParty/caj2pdf", "--hidden-import", "HNParsePage", "--hidden-import", "pdfwutils", "--hidden-import", "jbigdec", "--hidden-import", "jbig2dec", "--hidden-import", "imagesize", "--collect-all", "PIL", "--add-binary", str(work/"libjbigdec.so")+":.", "--add-binary", str(work/"libjbig2codec.so")+":.", "Scripts/caj_worker.py")
run("ditto", work/"dist/caj-worker", tools/"caj-worker")

latex_environment = os.environ.copy()
latex_environment["TECTONIC_CACHE_DIR"] = str(work/"tex-cache")
output = work/"tex-output"
output.mkdir(exist_ok=True)
run(tectonic, "--untrusted", "--outdir", output, "Scripts/latex-support.tex", env=latex_environment)
for name in ("report.cls", "book.cls"):
    with (work/name).open("wb") as stream:
        run(tectonic, "-X", "bundle", "cat", name, env=latex_environment, stdout=stream)
files = sorted(p for p in (work/"tex-cache/bundles/data").rglob("*") if p.is_file())
digest = hashlib.sha256()
with zipfile.ZipFile(root/"latex-bundle.zip", "w", zipfile.ZIP_DEFLATED) as bundle:
    for path in files:
        contents = path.read_bytes()
        digest.update(path.name.encode()); digest.update(contents)
        bundle.writestr(path.name, contents)
    bundle.writestr("SHA256SUM", digest.hexdigest()+"\n")
print(f"Prepared {architecture} tools and an offline LaTeX bundle with {len(files)} resources.")
