import logging
import difflib
from typing import List, Dict

class SectionSplitter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def split(self, text: str, headings: List[Dict]) -> List[Dict]:
        lines = text.split("\n")
        sections = []
        current_section = {"title": None, "content": [], "page": 1}

        if not headings or not lines:
            self.logger.warning("No headings or lines found to split.")
            return []

        heading_texts = [h["text"].strip() for h in headings if h.get("text")]
        heading_map = {h["text"].strip(): h for h in headings if h.get("text")}
        used_headings = set()

        for i, line in enumerate(lines):
            line_stripped = line.strip()

            if not line_stripped:
                continue

            match = difflib.get_close_matches(line_stripped, heading_texts, n=1, cutoff=0.8)
            if match:
                heading = match[0]
                if heading in used_headings:
                    continue
                used_headings.add(heading)

                if current_section["title"] and current_section["content"]:
                    text_block = "\n".join(current_section["content"])
                    sections.append({
                        "title": current_section["title"],
                        "text": text_block,
                        "page": current_section["page"]
                    })

                current_section = {
                    "title": heading,
                    "content": [],
                    "page": heading_map[heading]["page"]
                }
            else:
                current_section["content"].append(line_stripped)

        if current_section["title"] and current_section["content"]:
            text_block = "\n".join(current_section["content"])
            sections.append({
                "title": current_section["title"],
                "text": text_block,
                "page": current_section["page"]
            })

        self.logger.info(f"✅ Split into {len(sections)} sections.")
        return sections
