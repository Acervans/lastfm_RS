import numpy as np
from db_utils import *
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

vec = CountVectorizer()
# vec = TfidfVectorizer()

# Generates a sparse matrix
text_matrix = vec.fit_transform(grouped_tags['tags'])

print('Computing cosine similarities', flush=True)

# Cosine similarities
sim = cosine_similarity(text_matrix, text_matrix, dense_output=False)

sim.tofile('cos_sim.csv', sep='\t')

# TODO Dict of track_id, idx -> compute dynamically for each user