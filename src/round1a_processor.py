import json
import logging

from src.pdf_extractor import PDFExtractor
from src.heading_detector import HeadingDetector
from monitoring.performance_tracker import PerformanceTracker


class Round1AProcessor:
    def __init__(self):
        self.extractor = PDFExtractor()
        self.heading_detector = HeadingDetector()

    def process(self, pdf_path: str, output_json: str):
        try:
            with PerformanceTracker():
                logging.info(f"📄 Processing PDF: {pdf_path}")

                title = self.extractor.get_title(pdf_path) or ""
                outline = self.heading_detector.detect(pdf_path)

                result = {
                    "title": title,
                    "outline": outline
                }

                with open(output_json, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2)

                logging.info(f"✅ Output written to {output_json}")

        except Exception as e:
            logging.error(f"❌ Error in Round1AProcessor: {e}")
            raise