#!/usr/bin/env python3
"""Build character dictionary for PaddleOCR recognition training.

Collects unique characters from:
- annotation Label.txt files (if present)
- plain-text corpus files (tlarta_all_pdfs/txt/)

Usage:
    python scripts/build_char_dict.py
    python scripts/build_char_dict.py --corpus tlarta_all_pdfs/txt --output data/char_dict_avar.txt
"""

from __future__ import annotations

import argparse
from pathlib import Path


def collect_from_label_files(annotations_dir: Path) -> set[str]:
    chars: set[str] = set()
    for label_file in annotations_dir.rglob("Label.txt"):
        for line in label_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "\t" not in line:
                continue
            _, text = line.split("\t", 1)
            chars.update(text)
    return chars


def collect_from_corpus(corpus_dir: Path) -> set[str]:
    chars: set[str] = set()
    if not corpus_dir.exists():
        return chars
    for txt_file in corpus_dir.glob("*.txt"):
        chars.update(txt_file.read_text(encoding="utf-8", errors="replace"))
    return chars


def write_dict(chars: set[str], output_path: Path) -> None:
    # PaddleOCR dict: one character per line, no empty lines
    ordered = sorted(c for c in chars if c not in "\r\n")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(ordered) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Avar character dictionary for PaddleOCR.")
    parser.add_argument(
        "--annotations",
        type=Path,
        default=Path("data/annotations"),
        help="Folder with PPOCRLabel exports (default: data/annotations)",
    )
    parser.add_argument(
        "--corpus",
        type=Path,
        default=Path("tlarta_all_pdfs/txt"),
        help="Folder with plain-text corpus (default: tlarta_all_pdfs/txt)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/char_dict_avar.txt"),
        help="Output dictionary path (default: data/char_dict_avar.txt)",
    )
    args = parser.parse_args()

    chars: set[str] = set()
    if args.annotations.exists():
        from_ann = collect_from_label_files(args.annotations)
        chars |= from_ann
        print(f"Annotations: {len(from_ann)} unique chars from {args.annotations}")

    from_corpus = collect_from_corpus(args.corpus)
    chars |= from_corpus
    print(f"Corpus: {len(from_corpus)} unique chars from {args.corpus}")

    if not chars:
        raise SystemExit("No characters collected. Check --annotations and --corpus paths.")

    write_dict(chars, args.output)
    print(f"Wrote {len(chars)} characters to {args.output.resolve()}")


if __name__ == "__main__":
    main()
