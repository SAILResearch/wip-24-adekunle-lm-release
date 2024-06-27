import pandas as pd

data = "/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/NLP_main_dataset.xlsx"

# Specify encoding as 'ISO-8859-1' or 'latin1'
df_prime = pd.read_excel(data)

columns = [
    'model_name', 'hidden_act', 'vocab_size', 'intermediate_size',
    'num_hidden_layers', 'model_type', 'hidden_size', 'num_attention_heads',
    'bits', 'quant_method', 'model_size_million', 'model_size_thousand',
    'model_card_status', 'model_repo_status', 'time_upload', 'pipeline_tag',
    'category', 'likes', 'downloads', 'library', 'model_license', 'datasets',
    'model_archi', 'model_authors', 'metric_types', 'metric_values',
    'model_last_updated', 'github_link', 'model_url', 'commit_message',
    'total_commit', 'commit_title', 'commit_date', 'commit_authors',
    'commit_id', 'discussion_title', 'total_discussion', 'pull_auth',
    'status', 'pull_created', 'total_contributors', 'model_contributors'
]

# Select desired columns
df_all = df_prime[columns]

# Convert 'model_size_million' to numeric type
df_all['model_size_million'] = pd.to_numeric(df_all['model_size_million'], errors='coerce')

# Drop rows where 'github_link' is NaN or contains 'none_github'
df_all = df_all.dropna(subset=['github_link'])
df_all = df_all[~df_all['github_link'].astype(str).str.contains('none_github')]

# Filter rows where 'model_size_million' is greater than or equal to 1
df = df_all[df_all["model_size_million"] >= 1]
df_low = df_all[df_all["model_size_million"] < 1]

print(len(df))
print(len(df_all))
print(df["github_link"])
