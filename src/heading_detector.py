import re
import logging
from typing import List, Dict
import fitz  # Needed for page-wise text access

class HeadingDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def detect(self, pdf_path: str) -> List[Dict]:
        headings = []

        doc = fitz.open(pdf_path)

        for page_number, page in enumerate(doc, start=1):
            lines = page.get_text("text").splitlines()

            for line in lines:
                clean_line = line.strip()
                if not clean_line:
                    continue

                # Skip all-uppercase short codes (e.g., "AFM1", "ABC", etc.)
                if clean_line.isupper() and len(clean_line) <= 6:
                    continue

                # Skip full dates
                if re.match(r"^\d{1,2}\s+[A-Z]{3,9}\s+\d{4}$", clean_line):
                    continue

                # Match numbered headings
                if re.match(r"^\d+(\.\d+)*\s+.+", clean_line):
                    level = clean_line.count('.') + 1
                    headings.append({
                        "level": f"H{level}",
                        "text": clean_line,
                        "page": page_number
                    })
                    continue

                # Optional: Capitalized short headings fallback
                if clean_line[0].isupper() and len(clean_line.split()) <= 6:
                    headings.append({
                        "level": "H1",
                        "text": clean_line,
                        "page": page_number
                    })

        self.logger.info(f"✅ Detected {len(headings)} headings.")
        return headings