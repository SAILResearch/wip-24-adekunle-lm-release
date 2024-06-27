import pandas as pd
import re
import os
import requests
from huggingface_hub import HfApi, get_repo_discussions
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from requests.exceptions import RequestException
import pytz
from huggingface_hub import ModelCard


hugging_token = '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'
api = HfApi(token=hugging_token)

data = "/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/new_data/no_size.csv"

df = pd.read_csv(data)

error_dict = {"Model Name": [], "Error": []}
# Define CSV file path
csv_file_path = "/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/new_data/no_size_base_model.csv"
nlp_data = []
for index, row in df.iterrows():
    owner = row['owner']
    model_name = row["model_name"]
    model_links = row['model_links']
    pipeline = row['type']
    size = row['size']
    url = f"https://huggingface.co/api/models/{model_name}"

    try:
        info = requests.get(url)
        model_info = api.model_info(model_name)
        info_json = info.json()
        try:
            base_model = info_json["config"]["model_type"]
        except KeyError:
            base_model = "none"

        try:
            archi = info_json["config"]["architectures"]
        except KeyError:
            archi = "none"




        nlp_data.append({
            "Owner": owner,
            "Model Name": model_name,
            "model_link": model_links,
            "Pipeline": pipeline,
            "size": size,
            "base_model" : base_model,
            "architecture" : archi
        })

        print(base_model)

    except Exception as e:
        # Log the model name and error message to the error_dict
        error_dict["Model Name"].append(model_name)
        error_dict["Error"].append(str(e))
        print(f"Model information not found for '{model_name}': {e}")
        continue

error_df = pd.DataFrame(error_dict)

# Save error_df to a CSV file
error_df.to_csv('/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/new_data//error_no_size_base_models.csv', index=False)



# Convert the list of dictionaries to a DataFrame
nlp_df = pd.DataFrame(nlp_data)

# Save the DataFrame to CSV after all data is collected
nlp_df.to_csv(csv_file_path, index=False)

print("CSV file saved successfully.")