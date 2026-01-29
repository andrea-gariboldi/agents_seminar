import pandas as pd
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

from utils.dataset_utils import get_columns_from_dataset, exclude_column_from_dataset

def evaluate_clustering(submission_path: str):
    print("==========Running Clustering Evaluation==========")
    try: 
        submission_df = pd.read_csv(submission_path)
        X = exclude_column_from_dataset(submission_df[get_columns_from_dataset("agents_workspace/data/ecoli.csv")], "seq_name")
        labels = submission_df['cluster_id']
        
        silhouette = silhouette_score(X, labels)
        davies_bouldin = davies_bouldin_score(X, labels)
        calinski_harabasz = calinski_harabasz_score(X, labels)

        print(f"Silhouette Score: {silhouette:.3f} (higher is better, max=1)")
        print(f"Davies-Bouldin Index: {davies_bouldin:.3f} (lower is better, min=0)")
        print(f"Calinski-Harabasz Score: {calinski_harabasz:.2f} (higher is better)")
        print("==========Clustering Evaluation Finished==========")
    except Exception as e:
        print("==========Clustering Evaluation Failed==========")
        print(e)