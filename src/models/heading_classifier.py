from src.heading_detector import HeadingDetector

class HeadingClassifier:
    def __init__(self):
        self.detector = HeadingDetector()

    def classify(self, line: str) -> bool:
        """Return True if the given line of text is a heading."""
        return bool(self.detector.pattern.match(line) or line.isupper())
