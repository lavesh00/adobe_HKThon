import logging

class SummaryGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate_summary(self, text: str) -> str:
        self.logger.info("📝 Generating summary...")
        sentences = text.split('.')
        summary = '.'.join(sentences[:3]).strip()
        return summary + '.' if summary else ""
