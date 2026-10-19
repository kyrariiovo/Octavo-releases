"""Local CAJ conversion worker using caj2pdf (GLWTPL) and PyMuPDF (AGPL).

Run in a per-document temporary directory. See ThirdParty/caj2pdf and
Resources/ConverterLicenses for upstream sources and license notices.
"""
import os
import sys
from pathlib import Path

import cajparser
import pymupdf


def repair_pdf(arguments, **_kwargs):
    # caj2pdf invokes `mutool clean` for xref repair. Use the same MuPDF engine
    # through its Python binding so the app does not depend on an external CLI.
    if len(arguments) != 4 or arguments[:2] != ["mutool", "clean"]:
        raise ValueError("Unsupported repair command")
    with pymupdf.open(arguments[2]) as document:
        document.save(arguments[3], garbage=4, deflate=True)
    return b""


def main():
    source, output = map(Path, sys.argv[1:3])
    cajparser.check_output = repair_pdf
    parser = cajparser.CAJParser(str(source))
    parser.convert(str(output))
    if not output.is_file():
        raise ValueError("Unsupported CAJ structure")
    with pymupdf.open(output) as document:
        if document.page_count == 0 or document.needs_pass:
            raise ValueError("Invalid PDF output")


if __name__ == "__main__":
    try:
        main()
    except (Exception, SystemExit) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
