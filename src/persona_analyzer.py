import spacy
import logging

class PersonaAnalyzer:
    """
    Analyzes a user persona description to extract key terms and concepts
    using natural language processing.
    """
    def __init__(self):
        """
        Initializes the spaCy NLP model.
        This may download the model on first run if not already present.
        """
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logging.error("Spacy model 'en_core_web_sm' not found.")
            logging.info("Please run: python -m spacy download en_core_web_sm")
            raise

    def extract_keywords(self, persona_desc: str) -> list:
        """
        Extracts relevant keywords from a persona description.

        It prioritizes named entities (like organizations, products, people).
        If no entities are found, it falls back to extracting nouns and
        proper nouns as keywords.

        Args:
            persona_desc: A string containing the user persona description.

        Returns:
            A list of keyword strings.
        """
        doc = self.nlp(persona_desc)
        
        # First, try to extract named entities as they are often the most important keywords
        ents = [ent.text.lower() for ent in doc.ents]
        if ents:
            logging.info(f"Extracted entities from persona: {ents}")
            return list(set(ents)) # Return unique entities
            
        # If no entities are found, fall back to nouns and proper nouns
        keywords = [token.lemma_.lower() for token in doc if token.pos_ in ["NOUN", "PROPN"]]
        logging.info(f"Extracted nouns/proper nouns from persona: {keywords}")
        return list(set(keywords)) # Return unique keywords