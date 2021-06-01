from surprise import SVD
from surprise import Dataset
from surprise import accuracy
from surprise import Reader
import pandas as pd
import numpy as np
import os
from surprise.model_selection import train_test_split

# Load the movielens-100k dataset (download it if needed),
file_path = os.path.realpath('./database/datasets/movielens_small/ratings.csv')
reader = Reader(line_format='user item rating timestamp', sep=',', skip_lines=1)

data = Dataset.load_from_file(file_path, reader=reader)
#data = Dataset.load_builtin('ml-100k')

trainset, testset = train_test_split(data, test_size=.25)

algo = SVD()
algo.fit(trainset)
predictions = algo.test(testset)
test = pd.DataFrame(predictions)
test = test.rename(columns={'uid':'userId', 'iid': 'movieId',
                            'r_ui':'actual', 'est':'prediction'})
cf_model = test.pivot_table(index='userId',
                            columns='movieId', values='prediction').fillna(0)

def get_users_predictions(user_id, n, model):
    recommended_items = pd.DataFrame(model.loc[user_id])
    recommended_items.columns = ["predicted_rating"]
    recommended_items = recommended_items.sort_values('predicted_rating', ascending=False)
    recommended_items = recommended_items.head(n)
    return recommended_items.index.tolist()

def get_recs(model, k):
    recs = []
    for user in model.index:
        cf_predictions = get_users_predictions(user, k, model)
        recs.append(cf_predictions)
    return recs

# Top-10 recommendations for each user
k = 10
recs = get_recs(cf_model, k)
recsdf = pd.DataFrame(recs)
recsdf.index = np.arange(1, len(recsdf)+1)
preds = pd.DataFrame(index=cf_model.index)
preds[f'Top-{k} Recommendation'] = recs
save_path = os.path.realpath('./database/datasets/movielens_small/recom_svd_ds1.csv')
recsdf.to_csv(save_path, sep=",",index=True)
print(preds)
