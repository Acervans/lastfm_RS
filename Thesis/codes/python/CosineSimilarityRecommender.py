from recbole.utils import InputType, ModelType
from recbole.data.dataset.dataset import Dataset
from recbole.model.abstract_recommender import GeneralRecommender
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
from sklearn.preprocessing import normalize
from sklearn.utils.extmath import safe_sparse_dot
import pandas as pd
import numpy as np
import torch

class CosineSimilarityRecommender(GeneralRecommender):
    """ Recommendations based on features' (tags) cosine similarities """
    input_type = InputType.PAIRWISE
    type = ModelType.TRADITIONAL

    def __init__(self, config, dataset: Dataset):
        super(CosineSimilarityRecommender, self).__init__(config, dataset)
        # Model config, tag features, item indexing, similarity weights, topk cutoff, fake loss...
        ...
        # Set up vectorizer
        self.vectorizer = TfidfVectorizer(**config['Vectorizer_Config'], token_pattern=r"(?u)\b\w+\b", lowercase=False)
        # Vectorized item-tags matrix, vec_feat contains all the tag sequences
        self.vec_matrix = normalize(self.vectorizer.fit_transform(self.vec_feat))

    def cosine_similarity_scores(self, user_id):
        # User interactions indices
        users = self.inters[self.USER_ID]
        user_inters_idx = users == user_id.item()
        # Interacted items
        user_items = self.inters[self.ITEM_ID][user_inters_idx]
        # Item weights by rating
        weights = None
        if self.sim_weights is not None:
            weights = self.sim_weights[user_inters_idx]
            # Sort by weights for cutoff
            idx_by_weights = np.argsort(-weights)[:self.knn_topk]
            weights = weights[idx_by_weights]
            user_items = user_items[idx_by_weights]
        # Features to vectorize for user items
        items_idx = self.item_to_idx.loc[user_items.flatten()]
        rec_items_feat = self.vec_feat[items_idx]
        return self.feature_cosine_scores(rec_items_feat, items_idx, weights)

    def feature_cosine_scores(self, rec_items_feature, items_idx=None, item_weights=None):
        # Vectorize selected features
        rec_matrix = self.vectorizer.transform(rec_items_feature)
        # Compute cosine similarities with all items
        rec_matrix_norm = normalize(rec_matrix, copy=True)
        sims = safe_sparse_dot(self.vec_matrix, rec_matrix_norm.T, dense_output=True)
        # Cancel items used for recommendation
        if items_idx is not None:
            sims[items_idx] = 0
        # Average feature similarities
        return np.average(sims, weights=item_weights, axis=1)

    def calculate_loss(self, interaction): ...
    def predict(self, interaction): ...
    def full_sort_predict(self, interaction): ...