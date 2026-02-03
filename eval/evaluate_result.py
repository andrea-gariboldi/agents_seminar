import subprocess
import os

import pandas as pd
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

from utils.dataset_utils import get_columns_from_dataset, exclude_column_from_dataset
from utils.printing_utils import print_eval_message

def run_clustering_script(script_path: str) -> pd.DataFrame:
    script_dir = os.path.dirname(script_path)
    dataset_path = os.path.join(script_dir, 'data', 'ecoli.csv')
    try:
        subprocess.run(['conda', 'run', '-n', 'agents_env', 'python', script_path,
                        '--input', dataset_path, '--output', 'submission.csv'],
                        check=True, cwd=script_dir)
    except subprocess.CalledProcessError as e:
        print_eval_message("==========Clustering Script Failed to Run==========", True)
        print_eval_message(str(e), True)
        raise e
    submission_df = pd.read_csv(os.path.join(script_dir, 'submission.csv'))
    if not submission_df.empty:
        print_eval_message("The agent's script produced submission.csv successfully.")
    else:
        print_eval_message("==========Clustering Script Produced No Output==========", True)
    return submission_df

def evaluate_clustering(script_path: str):
    print_eval_message("==========Running Clustering Script==========")
    submission_df = run_clustering_script(script_path)
    print_eval_message("==========Finished Running Clustering Script==========")
    print_eval_message("==========Running Clustering Evaluation==========")
    try: 
        X = exclude_column_from_dataset(submission_df[get_columns_from_dataset("agents_workspace/data/ecoli.csv")], "seq_name")
        labels = submission_df['cluster_id']
        
        silhouette = silhouette_score(X, labels)
        davies_bouldin = davies_bouldin_score(X, labels)
        calinski_harabasz = calinski_harabasz_score(X, labels)

        print_eval_message(f"Silhouette Score: {silhouette:.3f} (higher is better, max=1)")
        print_eval_message(f"Davies-Bouldin Index: {davies_bouldin:.3f} (lower is better, min=0)")
        print_eval_message(f"Calinski-Harabasz Score: {calinski_harabasz:.2f} (higher is better)")
        print_eval_message("==========Clustering Evaluation Finished==========")
    except Exception as e:
        print_eval_message("==========Clustering Evaluation Failed==========", True)
        print_eval_message(str(e), True)