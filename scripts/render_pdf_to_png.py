#!/usr/bin/env python3
"""Render PDF files to PNG images (one file per page).

Usage:
    python scripts/render_pdf_to_png.py
    python scripts/render_pdf_to_png.py --input train_pdfs --output train_pdfs/img --dpi 200
"""

from __future__ import annotations

import argparse
from pathlib import Path

import fitz  # PyMuPDF


def render_pdf(pdf_path: Path, output_dir: Path, dpi: int) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    saved: list[Path] = []

    with fitz.open(pdf_path) as doc:
        stem = pdf_path.stem
        for page_index, page in enumerate(doc, start=1):
            pixmap = page.get_pixmap(matrix=matrix, alpha=False)
            out_path = output_dir / f"{stem}_page_{page_index:03d}.png"
            pixmap.save(out_path)
            saved.append(out_path)

    return saved


def main() -> None:
    parser = argparse.ArgumentParser(description="Render PDF files to PNG images.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("train_pdfs"),
        help="Folder with PDF files (default: train_pdfs)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("train_pdfs/img"),
        help="Folder for PNG output (default: train_pdfs/img)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="Render resolution in DPI (default: 200)",
    )
    args = parser.parse_args()

    pdf_files = sorted(args.input.glob("*.pdf"))
    if not pdf_files:
        raise SystemExit(f"No PDF files found in {args.input.resolve()}")

    total_pages = 0
    for pdf_path in pdf_files:
        saved = render_pdf(pdf_path, args.output, args.dpi)
        total_pages += len(saved)
        print(f"{pdf_path.name}: {len(saved)} page(s) -> {args.output}")

    print(f"Done. {len(pdf_files)} PDF(s), {total_pages} PNG file(s) in {args.output.resolve()}")


if __name__ == "__main__":
    main()
