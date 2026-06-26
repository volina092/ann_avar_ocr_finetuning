#!/usr/bin/env python3
"""Extract text lines with bounding boxes from PDF text layer.

Renders are not required for extraction, but this script can map PDF coordinates
to PNG pixel coordinates when a matching rendered page exists.

Output is a draft Label.txt + line crops for manual correction in PPOCRLabel.

Usage:
    python scripts/extract_pdf_text_layer.py --pdf train_pdfs/0_tlyarata_8_-na_pechat.pdf
    python scripts/extract_pdf_text_layer.py --pdf train_pdfs/0_tlyarata_8_-na_pechat.pdf --png train_pdfs/img/0_tlyarata_8_-na_pechat_page_001.png --dpi 200
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image


def group_words_into_lines(words: list[tuple], y_tol: float) -> list[list[tuple]]:
    """Group (x0, y0, x1, y1, text) word boxes into lines by vertical overlap."""
    if not words:
        return []
    words = sorted(words, key=lambda w: (w[1], w[0]))
    lines: list[list[tuple]] = []
    current: list[tuple] = [words[0]]
    for w in words[1:]:
        cy = (current[0][1] + current[0][3]) / 2
        wy = (w[1] + w[3]) / 2
        if abs(wy - cy) <= y_tol:
            current.append(w)
        else:
            lines.append(sorted(current, key=lambda x: x[0]))
            current = [w]
    lines.append(sorted(current, key=lambda x: x[0]))
    return lines


def pdf_to_png_scale(pdf_page: fitz.Page, png_path: Path) -> tuple[float, float]:
    """Return scale factors from PDF points to PNG pixels."""
    with Image.open(png_path) as img:
        pw, ph = img.size
    rect = pdf_page.rect
    return pw / rect.width, ph / rect.height


def extract_page_lines(
    pdf_path: Path,
    page_index: int,
    png_path: Path | None,
    dpi: int,
    y_tol: float,
) -> list[dict]:
    with fitz.open(pdf_path) as doc:
        page = doc[page_index - 1]
        words_raw = page.get_text("words")
        words = [(w[0], w[1], w[2], w[3], w[4]) for w in words_raw if w[4].strip()]
        line_groups = group_words_into_lines(words, y_tol=y_tol)

        if png_path and png_path.exists():
            sx, sy = pdf_to_png_scale(page, png_path)
        else:
            zoom = dpi / 72.0
            sx = sy = zoom

        lines: list[dict] = []
        for line_words in line_groups:
            text = " ".join(w[4] for w in line_words).strip()
            if not text:
                continue
            x0 = min(w[0] for w in line_words) * sx
            y0 = min(w[1] for w in line_words) * sy
            x1 = max(w[2] for w in line_words) * sx
            y1 = max(w[3] for w in line_words) * sy
            lines.append({"text": text, "bbox": [x0, y0, x1, y1]})
        return lines


def crop_and_save(
    png_path: Path,
    lines: list[dict],
    output_dir: Path,
    page_stem: str,
) -> list[str]:
    crop_dir = output_dir / "crop_img"
    crop_dir.mkdir(parents=True, exist_ok=True)
    label_entries: list[str] = []

    with Image.open(png_path).convert("RGB") as img:
        w, h = img.size
        for i, line in enumerate(lines, start=1):
            x0, y0, x1, y1 = line["bbox"]
            x0, y0 = max(0, int(x0)), max(0, int(y0))
            x1, y1 = min(w, int(x1)), min(h, int(y1))
            if x1 <= x0 or y1 <= y0:
                continue
            crop = img.crop((x0, y0, x1, y1))
            name = f"line_{i:04d}.jpg"
            crop.save(crop_dir / name, quality=95)
            rel = f"crop_img/{name}"
            label_entries.append(f"{rel}\t{line['text']}")
    return label_entries


def main() -> None:
    parser = argparse.ArgumentParser(description="Draft OCR labels from PDF text layer.")
    parser.add_argument("--pdf", type=Path, required=True, help="Input PDF file")
    parser.add_argument("--page", type=int, default=1, help="1-based page index (default: 1)")
    parser.add_argument("--png", type=Path, default=None, help="Matching rendered PNG (optional)")
    parser.add_argument("--dpi", type=int, default=200, help="DPI used for PNG render (default: 200)")
    parser.add_argument("--y-tol", type=float, default=3.0, help="Line grouping tolerance in PDF points")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output folder (default: data/annotations/<pdf_stem>/page_XXX)",
    )
    args = parser.parse_args()

    if not args.pdf.exists():
        raise SystemExit(f"PDF not found: {args.pdf}")

    page_tag = f"page_{args.page:03d}"
    output_dir = args.output or Path("data/annotations") / args.pdf.stem / page_tag
    output_dir.mkdir(parents=True, exist_ok=True)

    lines = extract_page_lines(args.pdf, args.page, args.png, args.dpi, args.y_tol)
    meta_path = output_dir / "draft_lines.json"
    meta_path.write_text(json.dumps(lines, ensure_ascii=False, indent=2), encoding="utf-8")

    label_entries: list[str] = ["# DRAFT — проверьте и исправьте в PPOCRLabel перед обучением"]
    if args.png and args.png.exists():
        label_entries = ["# DRAFT — проверьте и исправьте в PPOCRLabel перед обучением"]
        label_entries.extend(crop_and_save(args.png, lines, output_dir, args.pdf.stem))

    label_path = output_dir / "Label.txt"
    label_path.write_text("\n".join(label_entries) + "\n", encoding="utf-8")

    print(f"PDF: {args.pdf.name} page {args.page}")
    print(f"Lines extracted: {len(lines)}")
    print(f"Draft JSON: {meta_path.resolve()}")
    print(f"Label file: {label_path.resolve()}")
    if not (args.png and args.png.exists()):
        print("PNG not provided — only draft_lines.json written (no crops).")


if __name__ == "__main__":
    main()
