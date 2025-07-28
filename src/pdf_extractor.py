import fitz  # PyMuPDF
import logging
import io
from PIL import Image
import pytesseract


class PDFExtractor:
    """
    Extracts text and title from PDF files.
    Falls back to OCR only if no embedded text is found.
    """

    def __init__(self, enable_ocr=True):
        self.enable_ocr = enable_ocr

    def extract_text(self, pdf_path: str) -> str:
        """
        Extracts all text from a PDF.
        Falls back to OCR if PDF has no embedded text and OCR is enabled.
        """
        text = ""
        try:
            doc = fitz.open(pdf_path)

            for page in doc:
                page_text = page.get_text("text").strip()
                if page_text:
                    text += page_text + "\n"

            # OCR fallback
            if not text.strip():
                if self.enable_ocr:
                    logging.warning(f"📄 No embedded text in {pdf_path}. Falling back to OCR.")
                    for i, page in enumerate(doc):
                        logging.info(f"OCR on page {i + 1}/{len(doc)} of {pdf_path}")
                        pix = page.get_pixmap()
                        img = Image.open(io.BytesIO(pix.tobytes("ppm")))
                        if img.mode != "RGB":
                            img = img.convert("RGB")
                        text += pytesseract.image_to_string(img) + "\n"
                else:
                    logging.warning(f"📄 No embedded text in {pdf_path}, and OCR is disabled.")
                    return ""
            return text.strip()

        except Exception as e:
            logging.error(f"❌ Failed to extract text from {pdf_path}: {e}")
            raise

    def get_title(self, pdf_path: str) -> str:
        """
        Extracts the largest font text from the first page as title.
        """
        try:
            doc = fitz.open(pdf_path)
            first_page = doc.load_page(0)
            blocks = first_page.get_text("dict")["blocks"]

            max_size = 0
            title_candidate = ""

            for block in blocks:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            size = span["size"]
                            text = span["text"].strip()

                            if len(text) > 5 and size > max_size:
                                max_size = size
                                title_candidate = text

            return title_candidate or "Untitled"

        except Exception as e:
            logging.error(f"❌ Failed to extract title from {pdf_path}: {e}")
            return "Untitled"
