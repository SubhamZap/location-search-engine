from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import load_npz
import pandas as pd
import joblib

tfidf_matrix_filename = 'model/tfidf_matrix.npz'
index_mapping_filename = 'model/index_mapping.pkl'
tfidf_vectorizer_filename = 'model/tfidf_vectorizer.pkl'

def load_sparse_csr(filename):
    return load_npz(filename)

# Query and Retrieve
def search_location(input_text, top_n=5):
    # Load precomputed vectors and metadata
    tfidf_matrix = load_sparse_csr(tfidf_matrix_filename)
    index_mapping = pd.read_pickle(index_mapping_filename)
    tfidf_vectorizer = joblib.load(tfidf_vectorizer_filename)
    result = []

    # Vectorize the input text
    input_vector = tfidf_vectorizer.transform([input_text])

    # Compute cosine similarity between input text vector and precomputed vectors
    similarity_scores = cosine_similarity(input_vector, tfidf_matrix).flatten()

    # Retrieve top results
    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    top_results = index_mapping.loc[top_indices]
    for res in top_results:
        result.append(
            {
                'entity_name': res
            }
        )
    return result