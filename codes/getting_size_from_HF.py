import pandas as pd
import requests
import traceback
from huggingface_hub import HfApi

hugging_token = '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'
api = HfApi(token=hugging_token)

data = "/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/nlp_more_than_1m.xlsx"

df = pd.read_excel(data)



updated_df = []

for index, row in df.iterrows():
    try:
        owner = row['owner']
        model = row['model']
        model_name = row["model_name"]
        print(f"Processing model: {model_name}")

        time_upload = row['time_upload']
        pipeline = row['pipeline_tag']
        category = row['category']
        github = row['github_link']
        init_size = row['model_size']
        url = f"https://huggingface.co/api/models/{model_name}"
        things = requests.get(url)
        model_json = things.json()
        safetensors_total = model_json.get("safetensors", {}).get("total", None)

        if safetensors_total is not None:
            # Convert to millions only if "total" key is found
            model_size_million = safetensors_total / 1_000_000
        else:
            model_size_million = 0

        if safetensors_total is not None:
            # Convert to millions only if "total" key is found
            model_size_thousand = safetensors_total / 1_000
        else:
            model_size_thousand = 0

        result = {
            'owner': owner,
            'model': model,
            'model_name': model_name,
            'time_upload': time_upload,
            'pipeline': pipeline,
            'category': category,
            'github': github,
            'init_size': init_size,
            'model_size_million': model_size_million,
            'model_size_thousand': model_size_thousand
        }
        updated_df.append(result)
        print(f"Successfully processed model: {model_name}")
    except Exception as e:
        print(f"Error extracting model data for {model_name}: {e}")
        traceback.print_exc()

df2 = pd.DataFrame(updated_df)

df2.to_excel("/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/updated_dataset.xlsx", index=None)

print(df2)
