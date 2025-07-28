import json
import logging
import tempfile
from datetime import datetime

from src.round1a_processor import Round1AProcessor
from src.section_splitter import SectionSplitter
from src.intelligence_engine import IntelligenceEngine
from src.summary_generator import SummaryGenerator
from monitoring.performance_tracker import PerformanceTracker


class Round1BProcessor:
    def __init__(self):
        self.round1a = Round1AProcessor()
        self.splitter = SectionSplitter()
        self.intel_engine = IntelligenceEngine()
        self.summarizer = SummaryGenerator()

    def process(self, input_files: list, persona: str, output_path: str, job_to_be_done: str = "AUTO-GENERATED"):
        try:
            with PerformanceTracker():
                logging.info(f"🔕 Processing files for Round1B: {input_files}")

                all_sections = []
                extracted_meta = []

                for file in input_files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmpfile:
                        self.round1a.process(file, tmpfile.name)

                        with open(tmpfile.name, 'r', encoding='utf-8') as f:
                            round1a_result = json.load(f)

                    full_text = self.round1a.extractor.extract_text(file)
                    logging.info(f"Extracted {len(full_text.strip())} characters from {file}")

                    if not full_text.strip():
                        logging.warning(f"No text extracted from {file}. Skipping.")
                        continue

                    title = round1a_result.get("title", "")
                    headings = round1a_result.get("outline", [])

                    if not headings:
                        logging.warning(f"No headings found in Round1A output for {file}. Skipping.")
                        continue

                    split_sections = self.splitter.split(full_text, headings)

                    if not split_sections:
                        logging.warning(f"No headings or lines found to split for {file}.")

                    for section in split_sections:
                        if not section.get("text", "").strip():
                            continue

                        section["document"] = file
                        all_sections.append(section)

                        extracted_meta.append({
                            "document": file,
                            "section_title": section["title"],
                            "page_number": section["page"],
                            "text": section["text"]
                        })

                if not all_sections:
                    logging.warning("No sections provided.")

                ranked = self.intel_engine.rank_sections(all_sections, persona)
                top_sections = ranked[:5]

                extracted = []
                analysis = []

                for idx, sec in enumerate(top_sections):
                    extracted.append({
                        "document": sec["document"],
                        "section_title": sec["title"],
                        "importance_rank": idx + 1,
                        "page_number": sec["page"]
                    })

                    summary = self.summarizer.generate_summary(sec["text"])
                    analysis.append({
                        "document": sec["document"],
                        "refined_text": summary,
                        "page_number": sec["page"]
                    })

                result = {
                    "metadata": {
                        "input_documents": input_files,
                        "persona": persona,
                        "job_to_be_done": job_to_be_done,
                        "processing_timestamp": datetime.now().isoformat()
                    },
                    "extracted_sections": extracted,
                    "subsection_analysis": analysis
                }

                with open(output_path, 'w', encoding='utf-8') as out:
                    json.dump(result, out, indent=2)

                logging.info(f"✅ Round1B output written to {output_path}")

        except Exception as e:
            logging.error(f"❌ Error in Round1BProcessor: {e}")
            raise