from recbole.utils import InputType, ModelType
from recbole.data.dataset.dataset import Dataset
from recbole.model.abstract_recommender import GeneralRecommender
from sklearn.preprocessing import normalize
from scipy.spatial.distance import cdist
import pandas as pd
import numpy as np
import torch
import tqdm

class SentimentKNNRecommender(GeneralRecommender):
    type = ModelType.TRADITIONAL
    input_type = InputType.PAIRWISE

    def __init__(self, config, dataset: Dataset):
        super(SentimentKNNRecommender, self).__init__(config, dataset)

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

        # Fake loss
        self.fake_loss = torch.nn.Parameter(torch.zeros(1))

        # Item id to idx mapping
        self.item_to_idx = pd.Series(range(len(item_feats[self.ITEM_ID])), index=item_feats[self.ITEM_ID])

        # Item VADSt features
        self.vadst = item_feats['vadst']
        if config['use_vadst_cols']:
            self.vadst = self.vadst[:, config['use_vadst_cols']]

        # Fill nans with column average
        nanmeans = np.nanmean(self.vadst, axis=0)
        self.vadst[np.isnan(self.vadst[:, 0]), :] = nanmeans

        self.vadst = normalize(self.vadst)
        self.sentiment_centroids = None

        self.other_parameter_name = ["sentiment_centroids"]

    def forward(self, user, item):
        pass

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

    def calculate_loss(self, interaction):
        return torch.nn.Parameter(torch.zeros(1))

    def sentiment_knn_scores(self, user_id, item_id=None):
        # User centroid
        user_centroid = self.sentiment_centroids[user_id.item()]

        # VADSt euclidean distances
        if not item_id:
            distances = cdist(self.vadst, [user_centroid], 'seuclidean')
        else:
            distances = cdist([self.vadst[item_id.item()]], [user_centroid], 'seuclidean')

        # Inverted average euclidean distances as similarities (weighted if applicable)
        scores = 1 / (1 + distances)

        return scores

    # user, batch items
    def predict(self, interaction):
        user = interaction[self.USER_ID]
        item = interaction[self.ITEM_ID]

        scores = self.sentiment_knn_scores(user[0], item[0])
        return torch.Tensor(scores)

    # batch users, all items
    def full_sort_predict(self, interaction):
        user = interaction[self.USER_ID]
        scores = []
        for uid in user:
            scores.append(self.sentiment_knn_scores(uid))

        return torch.Tensor(np.array(scores))
