# This is a sample Python script.
import os
from cmath import rect

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import pymupdf


def split_pdf_to_pages(input_path, output_folder):
    """
    Split a PDF file into individual pages.

    Args:
        input_path (str): Path to the input PDF file
        output_folder (str): Directory to save individual pages
    """
    # Open the PDF document
    pdf_document = pymupdf.open(input_path)

    # Create output folder if it doesn't exist
    import os
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through each page
    for page_num in range(len(pdf_document)):
        # Create a new PDF document for this page
        new_pdf = pymupdf.open()

        # Insert the current page into the new document
        new_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)

        # Save the single-page PDF
        output_path = os.path.join(output_folder, f"page_{page_num + 1:03d}.pdf")
        new_pdf.save(output_path)
        new_pdf.close()

    # Close the original document
    pdf_document.close()
    print(f"Successfully split PDF into {len(pdf_document)} pages")


def split_pdf_to_images(input_path, output_folder, image_format="PNG", dpi=150):
    """
    Convert PDF pages to image files.

    Args:
        input_path (str): Path to input PDF
        output_folder (str): Output directory
        image_format (str): Image format (PNG, JPEG, etc.)
        dpi (int): Resolution for images
    """
    pdf_document = pymupdf.open(input_path)

    os.makedirs(output_folder, exist_ok=True)

    for page_num in range(len(pdf_document)):
        page: pymupdf.Page = pdf_document[page_num]
        x1 = float(350.0)
        y1 = float(350.0)
        r : rect = pymupdf.Rect(0, 0,x1, y1)
        page.clip_to_rect(r)
        # Create transformation matrix for desired DPI
        mat = pymupdf.Matrix(dpi / 72, dpi / 72)

        # Render page to image
        pix: pymupdf.Pixmap = page.get_pixmap(matrix=mat)
        pix.set_origin(0,600)
        # Save image
        output_path = os.path.join(output_folder, f"page_{page_num + 1:03d}.{image_format.lower()}")
        pix.save(output_path)

    pdf_document.close()
    print(f"Converted {len(pdf_document)} pages to {image_format} images")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
    split_pdf_to_images("./sup-practice.pdf", "./output_images")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
