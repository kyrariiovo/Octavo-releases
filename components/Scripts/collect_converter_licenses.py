"""Collect license notices from the Python environment used to freeze the worker."""
import importlib.metadata
import platform
import shutil
import sys
from pathlib import Path

project = Path(__file__).resolve().parents[1]
destination = project / "Resources/ConverterLicenses"
destination.mkdir(parents=True, exist_ok=True)
for package, output in [
    ("PyPDF2", "PyPDF2.txt"), ("imagesize", "imagesize.txt"),
    ("Pillow", "Pillow.txt"), ("PyMuPDF", "PyMuPDF.txt"),
    ("PyInstaller", "PyInstaller.txt"),
]:
    distribution = importlib.metadata.distribution(package)
    licenses = [path for path in distribution.files
                if path.name.lower().startswith(("license", "copying"))
                and ".dist-info" in str(path)]
    if not licenses:
        raise RuntimeError("Missing license for " + package)
    (destination / output).write_text("\n\n".join(
        distribution.locate_file(path).read_text(encoding="utf-8") for path in licenses), encoding="utf-8")
python_license = Path(sys.base_prefix) / f"lib/python{sys.version_info.major}.{sys.version_info.minor}/LICENSE.txt"
if not python_license.exists():
    python_license = Path(sys.base_prefix) / "LICENSE.txt"
if not python_license.exists():
    raise RuntimeError("Python license not found in " + sys.base_prefix)
shutil.copyfile(python_license, destination / "Python.txt")
shutil.copyfile(project / "ThirdParty/caj2pdf/LICENSE", destination / "caj2pdf.txt")
shutil.copyfile(project / "ThirdParty/README.md", destination / "Sources-and-notices.md")
shutil.copyfile(project / "Resources/Converters" / platform.machine() / "LibreOffice.app/Contents/Resources/LICENSE", destination / "LibreOffice.txt")
print("Collected conversion-tool license notices.")
