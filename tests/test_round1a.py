import os
import ujson as json
import pytest
import fitz
from src.round1a_processor import Round1AProcessor


def create_test_pdf(path, title, heading, content):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), title)
    page.insert_text((50, 100), heading)
    page.insert_text((50, 150), content)
    doc.save(path)


def test_round1a_basic(tmp_path):
    # Create a simple PDF for testing
    pdf_file = tmp_path / "test.pdf"
    create_test_pdf(str(pdf_file), "TestTitle", "1. HeadingOne", "Sample content.")

    output_json = tmp_path / "output.json"
    processor = Round1AProcessor()
    processor.process(str(pdf_file), str(output_json))

    assert output_json.exists()
    data = json.loads(output_json.read_text())
    assert "TestTitle" == data.get("title")
    headings = data.get("headings", [])
    assert any(h.get("text") == "1. HeadingOne" for h in headings)
