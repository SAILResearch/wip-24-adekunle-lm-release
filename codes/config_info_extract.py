import os
import pandas as pd
import traceback
from huggingface_hub import HfApi
#from transformers import AutoModel, AutoConfig

hugging_token = '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'
api = HfApi(token=hugging_token)

data = "/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/stage1_dataset.xlsx"

df = pd.read_excel(data)

small = df[0:100]

new_data = []

for index, row in df.iterrows():
    owner = row["owner"]
    model_name = row["model_name"]
    time_upload = row["time_upload"]
    pipeline_tag = row["pipeline_tag"]
    category = row["category"]
    github_link = row["github_link"]
    millions = row["millions"]
    billions = row["billions"]

    try:
        repo = api.repo_info(model_name)
        config = repo.config
        archi = config.get('architectures')
        base = config.get('model_type')
    except Exception as e:
        print(f"Error processing model {model_name}: {e}")
        traceback.print_exc()

    data = {
        'owner': owner,
        'model_name': model_name,
        'time_upload': time_upload,
        'pipeline_tag': pipeline_tag,
        'category': category,
        'github_link': github_link,
        'millions': millions,
        'billions': billions,
        'custom_archi': archi,
        'base': base,
    }
    new_data.append(data)
    #print(base)

new_d = pd.DataFrame(new_data)

new_d.to_excel("/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/stage2_dataset.xlsx", index=None)

print(new_d)


"""'owner', 'model_name', 'time_upload', 'pipeline_tag', 'category',
       'github_link', 'millions', 'billions'"""