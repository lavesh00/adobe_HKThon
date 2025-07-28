import os
import ujson as json
import pytest
import fitz
from src.round1b_processor import Round1BProcessor


def create_test_pdf(path, title, heading, content):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), title)
    page.insert_text((50, 100), heading)
    page.insert_text((50, 150), content)
    doc.save(path)


def test_round1b_basic(tmp_path):
    # Create two simple PDFs
    pdf1 = tmp_path / "doc1.pdf"
    pdf2 = tmp_path / "doc2.pdf"
    create_test_pdf(str(pdf1), "DocOneTitle", "1. Analysis", "Data about AI.")
    create_test_pdf(str(pdf2), "DocTwoTitle", "1. Summary", "Machine learning info.")

    persona = "Data scientist interested in machine learning and AI"
    output_json = tmp_path / "result.json"

    processor = Round1BProcessor()
    processor.process([str(pdf1), str(pdf2)], persona, str(output_json))

    assert output_json.exists()
    data = json.loads(output_json.read_text())
    matches = data.get("matches", [])

    assert isinstance(matches, list)
    # Expect at least one match entry
    assert len(matches) > 0
    # Check that explanation field is present
    assert "explanation" in matches[0]
