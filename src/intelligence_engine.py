import logging
from typing import List, Dict
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

class IntelligenceEngine:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.device = torch.device("cpu")
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2").to(self.device)

    def _embed(self, text: str) -> torch.Tensor:
        encoded = self.tokenizer(text, padding=True, truncation=True, return_tensors='pt').to(self.device)
        with torch.no_grad():
            output = self.model(**encoded)
        token_embeddings = output.last_hidden_state
        mask = encoded['attention_mask'].unsqueeze(-1).expand(token_embeddings.size()).float()
        return (token_embeddings * mask).sum(1) / mask.sum(1)

    def rank_sections(self, sections: List[Dict], persona: str) -> List[Dict]:
        if not sections:
            self.logger.warning("No sections provided.")
            return []

        # ✅ Corrected key from 'content' to 'text'
        texts = [s["text"] for s in sections if s.get("text", "").strip()]
        if not texts:
            self.logger.warning("All section texts empty.")
            return []

        # ✅ Filter the same list to avoid mismatch
        valid_sections = [s for s in sections if s.get("text", "").strip()]

        persona_vec = self._embed(persona)
        sec_vecs = torch.vstack([self._embed(txt) for txt in texts])
        sims = cosine_similarity(persona_vec.cpu().numpy().reshape(1, -1), sec_vecs.cpu().numpy())[0]

        for section, score in zip(valid_sections, sims):
            section["score"] = float(score)

        return sorted(valid_sections, key=lambda x: x["score"], reverse=True)
