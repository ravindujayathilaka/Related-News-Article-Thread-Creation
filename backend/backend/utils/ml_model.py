import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')

def extract_keywords(title):
    words = nltk.word_tokenize(title)
    keywords = [word for word in words if word.isalnum()]
    return keywords

def calculate_similarity(keywords1, keywords2):
    vectorizer = TfidfVectorizer().fit_transform([' '.join(keywords1), ' '.join(keywords2)])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0][1]
