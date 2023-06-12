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
    input_type = InputType.PAIRWISE
    type = ModelType.TRADITIONAL

    def __init__(self, config, dataset: Dataset):
        super(CosineSimilarityRecommender, self).__init__(config, dataset)

        # Set up vectorizer
        if config['Vectorizer'].lower() == 'countvectorizer':
            vectorizer = CountVectorizer
        elif config['Vectorizer'].lower() == 'tfidfvectorizer':
            vectorizer = TfidfVectorizer
        else:
            raise ValueError(f"Vectorizer {config['Vectorizer']} not valid.")
        
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

        # Set up column used for similarities
        self.vec_column = config['Vectorized_Column'] if 'Vectorized_Column' in config else 'tags'
        
        if dataset.field2seqlen[self.vec_column] == 1:
            self.vectorizer = vectorizer(**config['Vectorizer_Config'], token_pattern=r"(?u)\b\w+\b", lowercase=False)
        else:
            self.vectorizer = vectorizer(**config['Vectorizer_Config'], analyzer=lambda x: x)

        # Vectorized values from selected column
        self.vec_feat = item_feats[self.vec_column]

        # Item id to idx mapping
        self.item_to_idx = pd.Series(range(len(item_feats[self.ITEM_ID])), index=item_feats[self.ITEM_ID])

        # Item sequential token embedding
        self.vec_matrix = normalize(self.vectorizer.fit_transform(self.vec_feat))

    def forward(self, user, item):
        pass

    def calculate_loss(self, interaction):
        return torch.nn.Parameter(torch.zeros(1))

    def cosine_similarity_scores(self, user_id):
        # User interactions indices
        users = self.inters[self.USER_ID]
        user_inters_idx = users == user_id.item()
        
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

        # Features to vectorize for user items
        items_idx = self.item_to_idx.loc[user_items.flatten()]
        rec_items_feat = self.vec_feat[items_idx]
        
        return self.feature_cosine_scores(rec_items_feat, items_idx, weights)

    def feature_cosine_scores(self, rec_items_feature, items_idx=None, item_weights=None):
        # Vectorize items selected feature
        rec_matrix = self.vectorizer.transform(rec_items_feature)

        # Compute cosine similarities
        rec_matrix_norm = normalize(rec_matrix, copy=True)
        sims = safe_sparse_dot(self.vec_matrix, rec_matrix_norm.T, dense_output=True)

        # Cancel items used for recommendation
        if items_idx is not None:
            sims[items_idx] = 0

        # Average feature similarities (weighted if applicable)
        scores = np.average(sims, weights=item_weights, axis=1)

        return scores

    # user, batch items
    def predict(self, interaction):
        user = interaction[self.USER_ID]
        item = interaction[self.ITEM_ID]

        scores = self.cosine_similarity_scores(user[0])
        return scores[item[0].item()]

    # batch users, all items
    def full_sort_predict(self, interaction):
        user = interaction[self.USER_ID]
        scores = []
        for uid in user:
            scores.append(self.cosine_similarity_scores(uid))

        return torch.Tensor(np.array(scores))
