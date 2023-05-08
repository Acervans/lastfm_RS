import torch
import torch.nn as nn
from recbole.utils import InputType
from recbole.model.abstract_recommender import GeneralRecommender
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
import numpy as np

class CosineSimilarityRecommender(GeneralRecommender):
    input_type = InputType.PAIRWISE

    def __init__(self, config, dataset):
        super(CosineSimilarityRecommender, self).__init__(config, dataset)

        # Initialize variables
        self.item_features = None
        self.sim_matrix = None
        
        # Fake loss
        self.fake_loss = torch.nn.Parameter(torch.zeros(1))

        # Set up vectorizer
        if config['Vectorizer'].lower() == 'countvectorizer':
            self.vectorizer = CountVectorizer()
        elif config['Vectorizer'].lower() == 'tfidfvectorizer':
            self.vectorizer = TfidfVectorizer()
        else:
            raise ValueError(f"Vectorizer {config['Vectorizer']} not valid.")

        # Set up columns used for vectorizer
        self.vectorizer_columns = config['Vectorizer_Cols']

    def calculate_loss(self, interaction):
        return torch.nn.Parameter(torch.zeros(1))

    def init_weight(self):
        item_texts = [' '.join([str(self.dataset.get_item_feature(item_id, column)) for column in self.vectorizer_columns])
                      for item_id in range(self.n_items)]
        self.item_features = self.vectorizer.fit_transform(item_texts)
        self.sim_matrix = csr_matrix(np.eye(self.item_features.shape[0]))

    def forward(self, user, item):
        item_indices = self.interaction_matrix[user].indices
        item_similarities = self.sim_matrix[item_indices, item]
        if self.ratings is not None:
            item_ratings = self.ratings[user].toarray()[0][item_indices]
            item_similarities *= item_ratings
        return torch.sum(item_similarities)

    def predict(self, interaction):
        user = interaction[self.USER_ID]
        items = interaction[self.ITEM_ID]
        scores = []
        for item in items:
            score = self.forward(user, item)
            scores.append(score)
        return torch.tensor(scores)

    def full_sort_predict(self, interaction):
        user = interaction[self.USER_ID]
        items = self.dataset.item_pool
        scores = []
        for item in items:
            score = self.forward(user, item)
            scores.append(score)
        scores = torch.tensor(scores)
        _, indices = torch.sort(scores, descending=True)
        return indices