import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
from constants import ROOT


def recommender(recipe_id):
    recipe_features_df = pd.read_pickle(ROOT+'/resources/data.pkl')
    recipe_features_df_matrix = csr_matrix(recipe_features_df.values)

    model_knn = NearestNeighbors(n_neighbors=3, metric='cosine', algorithm='brute')
    model_knn.fit(recipe_features_df_matrix)

    query_index = recipe_id
    distances, indices = model_knn.kneighbors(recipe_features_df.iloc[query_index, :].values.reshape(1, -1),
                                              n_neighbors=6)

    recommendation_knn = []

    for i in range(0, len(distances.flatten())):
        if i != 0:
            recommendation_knn.append(recipe_features_df.index[indices.flatten()[i]])
    return recommendation_knn


if __name__ == '__main__':
    recommendations = recommender(30)
