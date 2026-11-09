#!/usr/bin/env python3
"""Verify the preserved archives and their contents without executing them."""

import argparse
import hashlib
from pathlib import Path
import sys
import zipfile


FILES = {
    "vendor/windows/BlackBerryFix.exe": "8dab7e156cf63062890e2eceda478d10de96d4918443422a7ee2740e860632a0",
    "vendor/windows/BlackBerryFix.zip": "74321fc83a8680a0a44ba6b842d1dc8883850b968414700b435dc2d93e3b8d67",
    "vendor/mac/KB36747_BlackBerryFixMac.zip": "201f1338e86980d5b5cbd318b750fad387cbc0cdd2e08eaacf4a9a5c9eba742c",
}

ARCHIVE_ENTRIES = {
    "vendor/windows/BlackBerryFix.zip": (
        "BlackBerryFix.exe",
        FILES["vendor/windows/BlackBerryFix.exe"],
    ),
    "vendor/mac/KB36747_BlackBerryFixMac.zip": (
        "BlackBerryFixMac",
        "2fbce57da2128e1890a140ca52ff6ddddc466aee681d88b325de49b488167021",
    ),
}


def sha256_stream(stream):
    digest = hashlib.sha256()
    for block in iter(lambda: stream.read(1024 * 1024), b""):
        digest.update(block)
    return digest.hexdigest()


def verify(root):
    ok = True
    for name, expected in FILES.items():
        try:
            with (root / name).open("rb") as stream:
                actual = sha256_stream(stream)
            if actual != expected:
                print("FAIL {}: SHA-256 mismatch ({})".format(name, actual))
                ok = False
            else:
                print("OK   {}".format(name))
        except OSError as error:
            print("FAIL {}: {}".format(name, error))
            ok = False

    for name, (entry_name, expected) in ARCHIVE_ENTRIES.items():
        try:
            with zipfile.ZipFile(root / name) as archive:
                if archive.namelist() != [entry_name]:
                    raise ValueError("unexpected archive entries")
                with archive.open(entry_name) as stream:
                    actual = sha256_stream(stream)
                if actual != expected:
                    raise ValueError("entry SHA-256 mismatch ({})".format(actual))
            print("OK   {} in {} (including ZIP CRC)".format(entry_name, name))
        except (OSError, zipfile.BadZipFile, RuntimeError, ValueError, KeyError) as error:
            print("FAIL {}: {}".format(name, error))
            ok = False
    return ok


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="project directory to check (defaults to this script's project)",
    )
    args = parser.parse_args()
    return 0 if verify(args.root) else 1


if __name__ == "__main__":
    sys.exit(main())
