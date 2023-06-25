import numpy as np
import torch

from recbole.model.general_recommender.itemknn import ItemKNN, ComputeSimilarity
from recbole.model.abstract_recommender import GeneralRecommender

class ItemKNNRecommender(ItemKNN):
    def __init__(self, config, dataset):
        GeneralRecommender.__init__(self, config, dataset)

        # load parameters info
        self.k = config["k"] or 100
        self.shrink = config["shrink"] if "shrink" in config else 0.0

        self.interaction_matrix = dataset.inter_matrix(form="csr").astype(np.float32)
        shape = self.interaction_matrix.shape
        assert self.n_users == shape[0] and self.n_items == shape[1]
        self.w = self.pred_mat = None

        self.fake_loss = torch.nn.Parameter(torch.zeros(1))
        self.other_parameter_name = ["w", "pred_mat"]

    def train(self, mode: bool = True):
        if self.pred_mat is None:
            _, self.w = ComputeSimilarity(
                self.interaction_matrix, topk=self.k, shrink=self.shrink
            ).compute_similarity("item")
            self.pred_mat = self.interaction_matrix.dot(self.w).tolil()

        super().train(mode)
