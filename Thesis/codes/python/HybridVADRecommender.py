from recbole.model.context_aware_recommender import PNN
from ItemKNNRecommender import ItemKNNRecommender
from recbole.data.dataset.dataset import Dataset
from sklearn.preprocessing import normalize
from scipy.spatial.distance import cdist
import pandas as pd
import numpy as np
import torch
import tqdm

class HybridVADRecommender(ContextAwareModel):
    """ Recommendations from averaging VAD distances with scores from other models """

    def __init__(self, config, dataset: Dataset):
        super().__init__(config, dataset)
        # Model config, VAD features, item indexing, similarity weights, topk cutoff, fake loss...
        ...
        # VAD centroids for all users
        self.sentiment_centroids = self.compute_sentiment_centroids()

    def compute_sentiment_centroids(self):
        # vadst contains VAD scores of every item
        sentiment_centroids = [np.array([0] * self.vadst.shape[1])]
        for user in tqdm.trange(1, self.n_users, desc='Computing user centroids'):
            user_inters_idx = self.inters[self.USER_ID] == int(user)
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
            # Average items VAD
            items_idx = self.item_to_idx.loc[user_items.flatten()]
            user_vads_centroid = np.average(self.vadst[items_idx], weights=weights, axis=0)
            sentiment_centroids.append(user_vads_centroid)
        return np.array(sentiment_centroids)

    def sentiment_knn_scores(self, user_id, item_id=None):
        user_centroid = self.sentiment_centroids[user_id.item()]
        # VADSt euclidean distances
        item_vadst = self.vadst if item_id is None else self.vadst[item_id.cpu().numpy()]
        distances = cdist(item_vadst, user_centroid.reshape(1, -1), 'seuclidean')
        # Inverted average euclidean distances as scores
        return 1 / (1 + distances)
    
    def hybrid_scores(self, model_scores, scores):
        model_scores = normalize(model_scores.cpu().detach().numpy().reshape(1, -1))
        scores = normalize(scores.reshape(1, -1))
        # Score similarities between both models
        sims = 1 / (1 + np.abs(scores - model_scores))
        # Add scores buffing similar ones
        return model_scores + (sims * scores)

    def predict(self, interaction): ...
    def full_sort_predict(self, interaction): ...