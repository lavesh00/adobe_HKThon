from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SemanticMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def similarity(self, text1: str, text2: str) -> float:
        tfidf = self.vectorizer.fit_transform([text1, text2])
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return float(sim)
