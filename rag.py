from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vectorizer = TfidfVectorizer()

def get_relevant_context(history, user_input, k=3):
    """Return the most relevant snippets for a user query."""
    texts = [msg.strip() for msg in history if isinstance(msg, str) and msg.strip()]
    if not texts:
        return []

    vectors = vectorizer.fit_transform(texts + [user_input])

    sims = cosine_similarity(vectors[-1], vectors[:-1])[0]
    top_k = min(k, len(texts))
    top_indices = sims.argsort()[-top_k:][::-1]

    return [texts[i] for i in top_indices]
