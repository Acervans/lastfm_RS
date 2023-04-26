from recbole.config import Config
from recbole.data import InputType, ModelType
from recbole.model.abstract_recommender import GeneralRecommender
import torch.nn as nn
import torch

class RandomRecommender(GeneralRecommender):
    input_type = InputType.POINTWISE
    type = ModelType.TRADITIONAL

    def __init__(self, config: Config, dataset):
        super(RandomRecommender, self).__init__(config, dataset)
        self.embedding_size = config['embedding_size'] or 64
        self.linear_layer = nn.Linear(self.n_items, self.embedding_size)

    def forward(self, user, item):
        scores = torch.rand(item.shape[0], self.n_items)
        return scores

    def calculate_loss(self, interaction):
        pos_items = interaction[self.ITEM_ID]
        neg_items = interaction[self.NEG_ITEM_ID]

        pos_scores = self.forward(interaction[self.USER_ID], pos_items)
        neg_scores = self.forward(interaction[self.USER_ID], neg_items)

        # We use the hinge loss function to calculate the loss
        loss = torch.nn.functional.relu(neg_scores - pos_scores + self.margin)
        return loss.mean()
    
    def predict(self, interaction):
        scores = torch.rand(self.n_items)
        return scores

    def full_sort_predict(self, interaction):
        scores = self.predict(interaction)
        return torch.argsort(-scores)
