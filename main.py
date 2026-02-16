
# Breaks up and orders pages of pdf's formatted to print as Tibetan Prayer booklets for Dakini Whisper
# https://www.dakiniswhisper.com/
import pymupdf
import os
from pathlib import Path


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
    if n > 2:  # Must be at keast 4 pages
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


def do_reformat_pdf(name):
    output_text_name = "ordered"+name
    split_pages_and_order(input_text_name, "output", output_text_name)
    print(f'Input {name} converted to {output_text_name}')  # Press ⌘F8 to toggle the breakpoint.


if __name__ == '__main__':
    input_text_name = "sup-practice.pdf"
    print(f'start to conver {input_text_name}...')

    do_reformat_pdf(input_text_name)
