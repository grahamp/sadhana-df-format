
# Breaks up and orders pages of pdf's formatted to print as Tibetan Prayer booklets for Dakini Whisper
#!/usr/bin/env python3
# Breaks up and orders pages of pdf's formatted to print as Tibetan Prayer booklets for Dakini Whisper
# https://www.dakiniswhisper.com/
import argparse
import os
from pathlib import Path

import pymupdf


def split_pages_and_order(input_path, output_folder, output_file,
                          name_prefix="page",
                          page_range=None,
                          preserve_bookmarks=False):
    pdf_document = pymupdf.open(input_path)

    Path(output_folder).mkdir(parents=True, exist_ok=True)

    total_pages = len(pdf_document)
    if page_range:
        start_page, end_page = page_range
        start_page = max(1, start_page) - 1
        end_page = min(total_pages, end_page)
    else:
        start_page, end_page = 0, total_pages

    pages_split = 0
    new_pdf: pymupdf.Document = pymupdf.open()

    for page_num in range(start_page, end_page):
        src_page = pdf_document[page_num]

        # first cut Sadhana pdf pages in two pdf pages, so that each Sadhana page (1a, 1b, 2b, etc) is in its own PDF page.
        pr = src_page.rect  # full page rectangle in points
        # Optional: keep your custom width; otherwise use pr.x1
        clip_width = min(800, pr.width)
        x0 = pr.x0
        x1 = pr.x0 + clip_width

        mid_y = pr.y0 + pr.height / 2.0

        top_clip = pymupdf.Rect(x0, pr.y0, x1, mid_y)
        bottom_clip = pymupdf.Rect(x0, mid_y, x1, pr.y1)
        # Make a new doc with each original pdf page cropped twice, making a new top page and bottom page.
        for clip in (top_clip, bottom_clip):
            out_page = new_pdf.new_page(width=clip.width, height=clip.height)
            out_page.show_pdf_page(
                pymupdf.Rect(0, 0, clip.width, clip.height),
                pdf_document,
                page_num,
                clip=clip
            )
            pages_split += 1
    # Now we have a new pdf doc with 2x the pages...

    # Reorder: move every 4th page (4, 8, 12, ...) to be between page 1 and 2
    n = len(new_pdf)
    if n > 2:  # Must be at least 4 pages
        # make a list of current indexes to capture the desired order, Used below..
        new_order = list()
        for page_num in range(n):
            if((page_num+1) %4 == 0) and not (page_num == 0) :
                new_order.append(page_num-3)
                new_order.append(page_num)
                new_order.append(page_num-2)
                new_order.append(page_num-1)
         # Do remaining pages
        remaining_pages = list(range(n - 4, n))
        new_order.extend(remaining_pages)
    else:
        new_order = list(range(n))

    reordered_pdf = pymupdf.open()
    for i in new_order: #generate our new order
        reordered_pdf.insert_pdf(new_pdf, from_page=i, to_page=i)

    output_path = os.path.join(output_folder, output_file)
    reordered_pdf.save(output_path)

    reordered_pdf.close()
    new_pdf.close()
    pdf_document.close()
    print(f"Successfully split {pages_split} pages from {input_path}")
    return pages_split


def do_reformat_pdf(input_path: str):
    input_name = Path(input_path).name
    output_text_name = "ordered_" + input_name
    split_pages_and_order(input_path, "output", output_text_name)
    print(f"Input {input_name} converted to {output_text_name}")


def _parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Split and reorder pages of a PDF for booklet printing."
    )
    parser.add_argument(
        "input_path",
        nargs="?",
        help="Path to the PDF to re-order",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = _parse_args(argv)

    if not args.input_path:
        print(" A path to a pdf to re-order should be provided")
        return 2

    print(f"start to conver {args.input_path}...")
    do_reformat_pdf(args.input_path)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
