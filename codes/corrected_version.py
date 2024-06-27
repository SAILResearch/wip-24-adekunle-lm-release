import pandas as pd
import requests
from huggingface_hub import HfApi, get_repo_discussions

hugging_token = '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'
api = HfApi(token=hugging_token)

data = "/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/new_data/comprehensive_dataset.csv"

df = pd.read_csv(data)

small = df[52100:]

# Define CSV file path
csv_file_path = "/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/new_data/commit_authors_extraction.csv"

the_authors = []
each_uniwut_author = []
error_dict = {"Model Name": [], "Error": []}

# Iterate over each row
for index, row in small.iterrows():
    owner = row['Owner']
    model_name = row["model_name"]
    model_links = row['model_link']
    url = f"https://huggingface.co/api/models/{model_name}"

    try:
        info = requests.get(url)
        model_info = api.model_info(model_name)
        info_json = info.json()
        commits = api.list_repo_commits(model_name)
        commit_author = [commit.authors for commit in commits]
        all_authors = [author for commit in commits for author in commit.authors]
        discussions = get_repo_discussions(model_name)
        disc_author = [disc.author for disc in discussions]
        unique_author = set(all_authors)
        the_authors.append(all_authors)

        # Save the data for this row to the CSV file
        with open(csv_file_path, 'a', newline='') as f:
            pd.DataFrame({
                "Owner": [owner],
                "model_name": [model_name],
                "model_link": [model_links],
                "all_authors": [all_authors],
                "unique_author": [unique_author],
                "discussion_author": [disc_author]
            }).to_csv(f, header=f.tell()==0, index=False)

        print(f"Processed {index + 1}/{len(df)} rows and pull_author {disc_author}")

    except Exception as e:
        # Log the model name and error message to the error_dict
        error_dict["Model Name"].append(model_name)
        error_dict["Error"].append(str(e))
        print(f"Model information not found for '{model_name}': {e}")
        continue

# Save error_df to a CSV file
error_df = pd.DataFrame(error_dict)
error_df.to_csv('/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/new_data//error_commit_error_authors.csv', index=False)

print("CSV file saved successfully.")
