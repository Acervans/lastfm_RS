from recbole.model.abstract_recommender import ContextAwareMixin
from recbole.model.context_aware_recommender import xDeepFM

import torch
import torch.nn.functional as F

class xDeepFMContextAware(ContextAwareMixin, xDeepFM):
    
    def __init__(self, config, dataset):
        super().__init__(config, dataset)
        
        self.vadst_embedding = torch.nn.Embedding(
            dataset.item_vadst_feat.field_size['vadst'], 
            config.embedding_size, 
            padding_idx=0
        )
        
    def forward(self, interaction):
        vadst = interaction[self.ITEM_FEAT_FIELDS]['vadst']   # (batch_size, field_size)
        vadst_emb = self.vadst_embedding(vadst)   # (batch_size, field_size, embedding_size)
        
        embedding_dict = self.get_embedding_dict(interaction)
        embedding_list = self.embedding_list(embedding_dict)
        x_deep = self.xDeep(embedding_list)
        xfm = self.fm(embedding_list)
        
        x = torch.cat([x_deep, xfm], dim=1)
        x = self.mlp(x)
        x = self.predict_layer(x)
        
        return x, vadst_emb
    
    def predict(self, interaction):
        scores, vadst_emb = self.forward(interaction)
        user = interaction[self.USER_ID]
        pos_items = interaction[self.POS_ITEM_ID]
        pos_ratings = interaction[self.POS_ITEM_RATINGS]
        pos_vadst = vadst_emb[:, self.item2id(pos_items), :]   # (batch_size, num_pos_items, embedding_size)
        dist = F.pairwise_distance(vadst_emb.unsqueeze(1), pos_vadst, p=2)   # (batch_size, num_pos_items, field_size)
        weights = 1.0 / (1.0 + dist)
        scores = (scores * weights * pos_ratings.unsqueeze(1)).sum(dim=1)
        
        return scores
    
    def full_sort_predict(self, interaction):
        scores, vadst_emb = self.forward(interaction)
        user = interaction[self.USER_ID]
        pos_items = interaction[self.POS_ITEM_ID]
        pos_ratings = interaction[self.POS_ITEM_RATINGS]
        pos_vadst = vadst_emb[:, self.item2id(pos_items), :]   # (batch_size, num_pos_items, embedding_size)
        dist = F.pairwise_distance(vadst_emb.unsqueeze(1), pos_vadst, p=2)   # (batch_size, num_pos_items, field_size)
        weights = 1.0 / (1.0 + dist)
        scores = (scores * weights * pos_ratings.unsqueeze(1)).sum(dim=1)
        
        return scores
