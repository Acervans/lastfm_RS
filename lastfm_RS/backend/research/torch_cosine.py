import numpy as np
import pandas as pd
from db_utils import *
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
from torch.nn.functional import cosine_similarity

grouped_tags = pd.read_csv("../data/recsys_data/track_full_data.zip", sep='\t')[['track_id', 'tags']].dropna().reset_index(drop=True)
track_to_idx = pd.Series(grouped_tags.index, index=grouped_tags['track_id'])

grouped_tags

# vec = CountVectorizer()
vec = TfidfVectorizer()

# Generates a sparse matrix
text_matrix = vec.fit_transform(grouped_tags['tags'])

# Cosine similarities
sim = cosine_similarity(text_matrix, text_matrix)



sim.tofile('cos_sim.csv', sep='\t')

# TODO Dict of track_id, idx -> compute dynamically for each user