# Sadhana PDF Format (CLI)

Breaks up and orders pages of PDFs formatted to print as Tibetan Prayer booklets for Dakini Whisper
https://www.dakiniswhisper.com/

 A path to a pdf to re-order should be provided
python3 ./main.py ./your.pdf
python3 ./main.py ~/Downloads/___Double-VYCurrent-pechaCurrent-April2022.pdf
python3 ./main.py ./vy.pdf

The output will be in ./output with "ordered_" prepended to the name

## Requirements

- Python 3
- Dependencies listed in `requirements.txt` (uses `pymupdf`)

## Setup

chmod +x setup.sh
run setup.sh
Creates and activates a virtual environment , then install dependencies:


