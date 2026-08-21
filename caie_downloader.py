#!/usr/bin/env python3
"""
CAIE PastPaperOpener - Linux port
==================================
Downloads ALL question papers (qp), mark schemes (ms) and inserts (in)
for a CAIE subject by entering just the subject code (e.g. 9702 for Physics
or 0448 for IGCSE Pakistan Studies).

Files are saved into an organised folder tree:
    Past Papers/<SUBJECT>/<YEAR>/<Session>/<...>.pdf

Run:
    python3 caie_downloader.py            # interactive
    python3 caie_downloader.py 9702       # default years
    python3 caie_downloader.py 9702 2020-2024
    python3 caie_downloader.py 9702 --all # every year
    python3 caie_downloader.py 0448 2024 --no-in   # skip inserts
"""

import argparse
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import urllib.request

BASE_URL = "https://pastpapers.papacambridge.com/directories/CAIE/CAIE-pastpapers/upload/%s"
CURRENT_YEAR = 2026

SESSIONS = ["m", "s", "w"]  # Feb/Mar, May/June, Oct/Nov
SESSION_NAMES = {"m": "FebMarch", "s": "MayJune", "w": "OctNov"}

# Two-digit "paper+variant" codes used from ~2014 onwards.
PAPERS_2D = ["01", "02", "03", "04", "11", "12", "13", "21", "22", "23", "31", "32", "33", "41", "42", "43"]
# Single-digit variant codes used by older papers.
PAPERS_1D = ["1", "2", "3", "4"]


def paper_url(subject, session, year2, kind, variant):
    return BASE_URL % f"{subject}_{session}{year2}_{kind}_{variant}.pdf"


PDF_MAGIC = b"%PDF-"


def is_pdf_file(path):
    """Return True if the file on disk is a real PDF (starts with %PDF)."""
    try:
        with open(path, "rb") as fh:
            return fh.read(len(PDF_MAGIC)) == PDF_MAGIC
    except Exception:
        return False


def is_available(url):
    """Return True if the remote URL actually serves a PDF.

    PapaCambridge returns HTTP 302 (redirecting to its homepage HTML) for
    papers that do not exist, and urllib follows that redirect transparently,
    so checking only the status code is not enough. We instead read the first
    bytes and require the PDF magic signature.
    """
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            head = resp.read(len(PDF_MAGIC))
            return head == PDF_MAGIC
    except Exception:
        return False


def download(url, dest):
    """Download url to dest. Returns True only if a valid PDF was saved.

    Files whose content is not a real PDF (e.g. the HTML homepage that
    PapaCambridge serves instead of a 404) are deleted and ignored.
    """
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_name(dest.name + ".part")
        with urllib.request.urlopen(req, timeout=120) as resp, open(tmp, "wb") as fh:
            head = resp.read(len(PDF_MAGIC))
            if head != PDF_MAGIC:
                return False
            fh.write(head)
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                fh.write(chunk)
        tmp.replace(dest)
        return True
    except Exception as e:
        print(f"    [fail] {dest.name}: {e}")
        return False
    finally:
        tmp = dest.with_name(dest.name + ".part")
        if tmp.exists():
            tmp.unlink()


def probe_year_session(subject, year2, session, kinds, workers=8):
    """Discover and download all available qp/ms for one year+session."""
    found = []
    candidates = []
    for kind in kinds:
        for v in PAPERS_2D + PAPERS_1D:
            url = paper_url(subject, session, year2, kind, v)
            candidates.append((url, kind, v))

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(is_available, url): (url, kind, v) for url, kind, v in candidates}
        for fut in as_completed(futures):
            url, kind, v = futures[fut]
            if fut.result():
                found.append((url, kind, v))
    return found


def main():
    parser = argparse.ArgumentParser(description="Download ALL CAIE qp & ms for subject code(s) on Linux.")
    parser.add_argument("tokens", nargs="*", help="Subject code(s) and optional year range, e.g. 9702 0450 2020-2024")
    parser.add_argument("--all", action="store_true", help="Search every year the subject exists")
    parser.add_argument("--qp", action="store_true", help="Only download question papers")
    parser.add_argument("--ms", action="store_true", help="Only download mark schemes")
    parser.add_argument("--in", action="store_true", dest="ins", help="Only download inserts")
    parser.add_argument("--no-in", action="store_false", dest="ins", help="Do not download inserts")
    parser.set_defaults(ins=None)
    parser.add_argument("--workers", type=int, default=16, help="Parallel downloads (default 16)")
    args = parser.parse_args()

    # Separate the year range token from subject codes.
    # A 4-digit token is treated as a subject code; a 2-digit token or
    # "YYYY-YYYY" range is the year selection.
    subjects = []
    years_arg = None
    for tok in args.tokens:
        if tok.isdigit() and len(tok) == 4:
            subjects.append(tok)
        elif re.fullmatch(r"\d{4}-\d{4}", tok):
            years_arg = tok
        elif tok.isdigit() and len(tok) == 2:
            years_arg = tok
        else:
            print(f"Ignoring unrecognised token: {tok!r}")

    while not subjects:
        users = input("Enter subject code(s), space separated (e.g. 9702 0450): ").strip().split()
        for tok in users:
            if tok.isdigit() and len(tok) == 4:
                subjects.append(tok)
            else:
                print(f"Ignoring invalid subject code: {tok!r}")

    processed = list(dict.fromkeys(subjects))
    if not processed:
        sys.exit("No valid subject codes given.")

    kinds = []
    if args.qp:
        kinds.append("qp")
    if args.ms:
        kinds.append("ms")
    if args.ins:
        kinds.append("in")
    if not kinds:
        kinds = ["qp", "ms", "in"] if args.ins is not False else ["qp", "ms"]

    # Resolve the year list.
    years = []
    if args.all:
        years = list(range(2002, CURRENT_YEAR + 1))
    elif years_arg:
        try:
            if "-" in years_arg:
                start, end = years_arg.split("-", 1)
                years = list(range(int(start), int(end) + 1))
            else:
                years = [int(years_arg)]
        except ValueError:
            print("Invalid year range. Use e.g. 2019-2023 or 2022")
            sys.exit(1)
    else:
        default_end = CURRENT_YEAR
        default_start = max(2002, default_end - 10)
        print(f"\nNo year range given. Using last 10 years ({default_start}-{default_end}).")
        print("Tip: pass a range like `9702 2015-2024` or use `--all` for every year.")
        years = list(range(default_start, default_end + 1))

    years = sorted(y for y in years if 0 <= y <= 9999)
    year2_list = [f"{y:02d}"[-2:] for y in years]
    # Deduplicate identical last-two-digit years in one go.
    year2_list = list(dict.fromkeys(year2_list))

    print(f"\nSubjects : {', '.join(processed)}")
    print(f"Types    : {', '.join(kinds)}")
    print(f"Years    : {', '.join(year2_list)}")
    print(f"Workers  : {args.workers}")

    for subject in processed:
        run_subject(subject, year2_list, kinds, args.workers)


def run_subject(subject, year2_list, kinds, workers):
    root = Path("Past Papers") / subject
    total_downloaded = 0
    total_skipped = 0

    print(f"\n### Subject {subject} ###")
    print(f"Dest : {root.resolve()}\n")

    for year2 in year2_list:
        for session in SESSIONS:
            print(f"[20{year2} {SESSION_NAMES[session]}] probing...", end=" ", flush=True)
            hits = probe_year_session(subject, year2, session, kinds, workers=workers)
            if not hits:
                print("no papers found")
                continue
            print(f"{len(hits)} found, downloading")
            session_dir = SESSION_NAMES[session]
            for url, kind, v in hits:
                dest = root / f"20{year2}" / session_dir / f"{subject}_{session}{year2}_{kind}_{v}.pdf"
                if dest.exists() and dest.stat().st_size > 0 and is_pdf_file(dest):
                    print(f"    [skip] {dest.name} (already present)")
                    total_skipped += 1
                    continue
                if dest.exists():
                    dest.unlink()
                print(f"    [get ] {dest.name}", flush=True)
                if download(url, dest):
                    total_downloaded += 1
                else:
                    print(f"    [!!  ] {dest.name} is not a valid PDF, skipped")
            time.sleep(0.2)

    print(f"\nDone. {total_downloaded} downloaded, {total_skipped} skipped -> {root.resolve()}")

    removed = cleanup_invalid(root)
    if removed:
        print(f"Cleaned up {removed} leftover non-PDF file(s) from previous runs.")


def cleanup_invalid(root):
    """Delete leftover files mislabeled .pdf that are not real PDFs."""
    removed = 0
    if root.exists():
        for path in root.rglob("*.pdf"):
            if not is_pdf_file(path):
                try:
                    path.unlink()
                    removed += 1
                except OSError:
                    pass
    return removed


if __name__ == "__main__":
    main()
