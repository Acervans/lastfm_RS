# -*- coding: utf-8 -*-
# @Author : Javier Wang

import torch

from recbole.model.abstract_recommender import GeneralRecommender
from recbole.utils import InputType, ModelType


class RandomRecommender(GeneralRecommender):
    """ Random recommendations as baseline for performance comparison """
    rand_scores: torch.Tensor
    input_type = InputType.POINTWISE
    type = ModelType.TRADITIONAL

    def __init__(self, config, dataset: Dataset):
        super(RandomRecommender, self).__init__(config, dataset)
        # Initial random scores
        self.generate_random_scores()
        # Fake loss parameter
        self.fake_loss = torch.nn.Parameter(torch.zeros(1))

    def calculate_loss(self, interaction):
        # Re-randomize scores
        self.generate_random_scores()
        return torch.nn.Parameter(torch.zeros(1))

    def predict(self, interaction, generate_new=False):
        if generate_new:
            self.generate_random_scores()
        item = interaction[self.ITEM_ID]
        return self.rand_scores[item, :].squeeze(-1)

    def full_sort_predict(self, interaction, generate_new=False):
        if generate_new:
            self.generate_random_scores()
        batch_user_num = interaction[self.USER_ID].shape[0]
        result = torch.repeat_interleave(self.rand_scores.unsqueeze(0), batch_user_num, dim=0)
        return result.view(-1)

    def generate_random_scores(self):
        # Generate random tensor of scores
        self.rand_scores = torch.rand(self.n_items, 1, device=self.device)
