from recbole.model.context_aware_recommender import PNN
from ItemKNNRecommender import ItemKNNRecommender
from recbole.data.dataset.dataset import Dataset
from sklearn.preprocessing import normalize
from scipy.spatial.distance import cdist
import pandas as pd
import numpy as np
import torch
import tqdm

class LastFMRecommender(PNN):

    def __init__(self, config, dataset: Dataset):
        super().__init__(config, dataset)

        # load dataset info
        self.USER_ID = config["USER_ID_FIELD"]
        self.ITEM_ID = config["ITEM_ID_FIELD"]
        self.NEG_ITEM_ID = config["NEG_PREFIX"] + self.ITEM_ID
        self.n_users = dataset.num(self.USER_ID)
        self.n_items = dataset.num(self.ITEM_ID)

        # load parameters info
        self.device = config["device"]

        if isinstance(dataset.inter_feat, pd.DataFrame):
            self.inters = {col: dataset.inter_feat[col].values for col in dataset.inter_feat.columns}
            item_feats = dataset.get_item_feature()
            item_feats = {col: item_feats[col].values for col in item_feats.columns}
        else:
            self.inters = dataset.inter_feat.numpy()
            item_feats = dataset.get_item_feature().numpy()

        self.knn_topk = config['knn_topk'] if config['weighted_average'] else None

        # Ratings as weights
        if 'rating' in self.inters and config['weighted_average']:
            # Avoid division by 0
            self.sim_weights = np.add(self.inters['rating'], 1)
        else:
            self.sim_weights = None

        # Item id to idx mapping
        self.item_to_idx = pd.Series(range(len(item_feats[self.ITEM_ID])), index=item_feats[self.ITEM_ID])

        # Item VADSt features
        self.vadst = np.column_stack([item_feats['v'], item_feats['a'], item_feats['d'], item_feats['stsc']], axis=0)
        if config['use_vadst_cols']:
            self.vadst = self.vadst[:, config['use_vadst_cols']]

        # Fill nans with column average
        nanmeans = np.nanmean(self.vadst, axis=0)
        self.vadst[np.isnan(self.vadst[:, 0]), :] = nanmeans

        self.vadst = normalize(self.vadst)
        self.sentiment_centroids = None

        if hasattr(self, "other_parameter_name") and isinstance(self.other_parameter_name, list):
            self.other_parameter_name += ["sentiment_centroids"]
        else:
            self.other_parameter_name = ["sentiment_centroids"]

    def train(self, mode: bool = True):
        if self.sentiment_centroids is None:
            self.compute_sentiment_centroids()
        return super().train(mode)

    def compute_sentiment_centroids(self):
        sentiment_centroids = [np.array([0] * self.vadst.shape[1])]

        for user in tqdm.trange(1, self.n_users, desc='Computing user centroids'):
            user_inters_idx = self.inters[self.USER_ID] == int(user)

            # Interacted items
            user_items = self.inters[self.ITEM_ID][user_inters_idx]

            # Weights by rating
            if self.sim_weights is not None:
                weights = self.sim_weights[user_inters_idx]

                # Sort by weights for cutoff
                idx_by_weights = np.argsort(-weights)[:self.knn_topk]
                weights = weights[idx_by_weights]

                user_items = user_items[idx_by_weights]
            else:
                weights = None

            items_idx = self.item_to_idx.loc[user_items.flatten()]

            user_vads_centroid = np.average(self.vadst[items_idx], weights=weights, axis=0)
            sentiment_centroids.append(user_vads_centroid)

        self.sentiment_centroids = np.array(sentiment_centroids)


    def sentiment_knn_scores(self, user_id, item_id=None):
        # User centroid
        user_centroid = self.sentiment_centroids[user_id.item()]

        # VADSt euclidean distances
        if item_id is None:
            distances = cdist(self.vadst, user_centroid.reshape(1, -1), 'seuclidean')
        else:
            distances = cdist(self.vadst[item_id.cpu().numpy()], user_centroid.reshape(1, -1), 'seuclidean')

        # Inverted average euclidean distances as similarities (weighted if applicable)
        scores = 1 / (1 + distances)

        return scores

    # user, batch items
    def predict(self, interaction):
        model_scores = super().predict(interaction).cpu()

        user = interaction[self.USER_ID]
        item = interaction[self.ITEM_ID]

        scores = self.sentiment_knn_scores(user[0], item)
        scores = self.hybrid_scores(model_scores, scores)

        return torch.Tensor(np.array(scores)).to(self.device)

    # batch users, all items
    def full_sort_predict(self, interaction):
        model_scores = super().full_sort_predict(interaction)

        user = interaction[self.USER_ID]
        scores = []
        for uid in user:
            scores.append(self.sentiment_knn_scores(uid))

        scores = np.array(scores)
        return torch.Tensor(self.hybrid_scores(model_scores, scores)).to(self.device)

    def hybrid_scores(self, model_scores, scores):
        model_scores = normalize(model_scores.cpu().detach().numpy().reshape(1, -1))
        scores = normalize(scores.reshape(1, -1))

        nan_idx = np.isnan(model_scores)
        model_scores[nan_idx] = scores[nan_idx]

        # Score similarities between both models
        sims = 1 / (1 + np.abs(scores - model_scores))

        # Add scores buffing similar ones
        return model_scores + (sims * scores)