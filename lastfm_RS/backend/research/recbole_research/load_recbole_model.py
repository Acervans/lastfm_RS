from recbole_run import load_data_and_model
from recbole.utils.case_study import full_sort_scores, full_sort_topk
from recbole.data.dataset.dataset import Dataset

import numpy as np

if __name__ == "__main__":

    dataset: Dataset
    # NOTE: solo para probar, borrar en cuanto este el view de django
    config, model, dataset, train_data, valid_data, test_data = load_data_and_model(
        model_file='saved/CosineSimilarityRecommender-May-24-2023_23-53-35.pth',
        update_config={
            'dataset_save_path': 'saved/lastfm_recbole-dataset.pth',
            'dataloaders_save_path': 'saved/lastfm_recbole-for-CosineSimilarityRecommender-dataloader.pth',
            # 'weighted_average': True,
            # 'knn_topk': 5
        },
        use_training=False,
        verbose=False,
    )

    uid_series = dataset.token2id(dataset.uid_field, ['216'])
    
    scores = model.full_sort_predict({dataset.uid_field: uid_series}).numpy().flatten()

    item_ids = dataset.id2token(dataset.iid_field, list(range(dataset.item_num)))
    
    sorted_idx = np.argsort(-scores)
    
    print(list(zip(scores[sorted_idx], item_ids[sorted_idx]))[:10])

    # topk_score, topk_iids = full_sort_topk(uid_series, model, test_data, 10, device=config['device'])
    
    # external_item_list = dataset.id2token(dataset.iid_field, topk_iids.cpu())
    # print(list(zip(topk_score[0], external_item_list[0])))