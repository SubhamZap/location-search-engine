from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import load_npz
import pandas as pd
import joblib
import json
import boto3
import numpy as np
from io import BytesIO
import pickle

s3 = boto3.client('s3')
bucket_name = 'location-search-model-weights'

def load_sparse_csr(filename):
    return load_npz(filename)

def load_data_from_s3(bucket_name, file_key):
    try:
        # Initialize Boto3 S3 client
        s3 = boto3.client('s3')
        
        # Load the file from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        body = response['Body'].read()
        return body
    except Exception as e:
        print(f"Error loading data from S3: {e}")
        return None

try:
    tfidf_matrix_filename = 'tfidf_matrix.npz'
    index_mapping_filename = 'index_mapping.pkl'
    tfidf_vectorizer_filename = 'tfidf_vectorizer.pkl'

    # s3.Bucket(bucket_name).download_file(tfidf_matrix_filename, tfidf_matrix_filename)
    # s3.Bucket(bucket_name).download_file(index_mapping_filename, index_mapping_filename)
    # s3.Bucket(bucket_name).download_file(tfidf_vectorizer_filename, tfidf_vectorizer_filename)

    # Load precomputed vectors and metadata
    tfidf_matrix_body = load_data_from_s3(bucket_name, tfidf_matrix_filename)
    if tfidf_matrix_body is not None:
        try:
            with BytesIO(tfidf_matrix_body) as bio_tfidf:
                npzfile = np.load(BytesIO(tfidf_matrix_body), allow_pickle=True)
                tfidf_matrix = npzfile['data']
            print("TF-IDF matrix loaded successfully.")
        except Exception as e:
            print(f"Error loading TF-IDF matrix: {e}")

    # body = s3.get_object(Bucket=bucket_name, Key=tfidf_matrix_filename)['Body'].read()
    # npzfile = np.load(BytesIO(body))
    # tfidf_matrix = npzfile['data']

    index_mapping_body = load_data_from_s3(bucket_name, index_mapping_filename)
    if index_mapping_body is not None:
        try:
            index_mapping = pickle.loads(index_mapping_body)
            print("Index mapping loaded successfully.")
        except Exception as e:
            print(f"Error loading index mapping: {e}")

    tfidf_vectorizer_body = load_data_from_s3(bucket_name, tfidf_vectorizer_filename)
    if tfidf_vectorizer_body is not None:
        try:
            with open('/tmp/tfidf_vectorizer.pkl', 'wb') as f:
                f.write(tfidf_vectorizer_body)
            tfidf_vectorizer = joblib.load('/tmp/tfidf_vectorizer.pkl')
            # tfidf_vectorizer = joblib.load(tfidf_vectorizer_body)
            print("tfidf vectorizer loaded successfully.")
        except Exception as e:
            print(f"Error loading tfidf vectorizer: {e}")

    # index_mapping = pickle.loads(s3.get_object(Bucket=bucket_name, Key=index_mapping_filename)['Body'].read())

    # tfidf_vectorizer = joblib.load(s3.get_object(Bucket=bucket_name, Key=tfidf_vectorizer_filename)['Body'].read())

    # with open(index_mapping_filename, 'rb') as file:
    #     index_mapping = pd.read_pickle(file)

    # with open(tfidf_vectorizer_filename, 'rb') as file:
    #     tfidf_vectorizer = joblib.load(tfidf_vectorizer_filename)

except Exception as e:
    print(f"Error fetching S3 object. Error: {e}")

# Query and Retrieve
def search_location(input_text, top_n=5):
    result = []

    # Vectorize the input text
    input_vector = tfidf_vectorizer.transform([input_text])
    print(input_vector.shape)
    # Compute cosine similarity between input text vector and precomputed vectors
    similarity_scores = cosine_similarity(input_vector, tfidf_matrix).flatten()

    # Retrieve top results
    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    top_results = index_mapping.iloc[top_indices]
    for res in top_results:
        result.append(res)
    return result

def handler(event, context):
    try:
        if 'body' in event:
            # Parse the JSON body
            request_body = json.loads(event['body'])
            input_text = request_body.get('input_text')
        else:
            # If no body is present, look for query parameters
            input_text = event.get('input_text')
        
        if input_text is None:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Missing required parameters: input_text'})
            }
        
        result = search_location(input_text=input_text)
        return {
            'statusCode': 200,
            'body': json.dumps({'similarity score': result})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'{e}'})
        }