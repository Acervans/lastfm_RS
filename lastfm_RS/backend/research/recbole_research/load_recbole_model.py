from recbole_run import load_data_and_model
from recbole.utils.case_study import full_sort_scores, full_sort_topk

if __name__ == "__main__":

    # NOTE: solo para probar, borrar en cuanto este el view de django
    config, model, dataset, train_data, valid_data, test_data = load_data_and_model(
        model_file='saved/CosineSimilarityRecommender-May-21-2023_03-45-47.pth',
        update_config=None,
        verbose=True,
    )

    uid_series = dataset.token2id(dataset.uid_field, ['216'])
    topk_score, topk_iids = full_sort_topk(uid_series, model, test_data, 10, device=config['device'])
    
    external_item_list = dataset.id2token(dataset.iid_field, topk_iids.cpu())
    print(list(zip(topk_score[0], external_item_list[0])))