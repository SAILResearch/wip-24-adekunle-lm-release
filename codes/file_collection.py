import pandas as pd
import requests
from huggingface_hub import HfApi, get_repo_discussions
from git import Repo
from git import Repo, NoSuchPathError
from bs4 import BeautifulSoup


hugging_token = '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'
api = HfApi(token=hugging_token)

data = "/Users/adekunleajibode/Desktop/CISC_877_doc/RQ1_Experiment/new_data/comprehensive_dataset.csv"

df = pd.read_csv(data)

small = df[0:10]



for index, row in small.iterrows():
    owner = row['Owner']
    model_name = row["model_name"]
    model_links = row['model_link']
    url = f"https://huggingface.co/api/models/{model_name}.git"
    files = api.list_repo_files(model_name)

    filtered_files = [file for file in files if file.endswith(('.bin', '.pt', '.pth', '.h5'))]

    for f in filtered_files:
        file_loc = f"https://huggingface.co/{model_name}/blob/main/{f}"
        response = requests.get(file_loc)
        if response.status_code == 200:
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            ul_tag = soup.find('ul', class_='break-words font-mono text-sm')
            if ul_tag:
                li_tags = ul_tag.find_all('li')
                for li in li_tags:
                    strong_tag = li.find('strong')
                    if strong_tag and strong_tag.text.strip() == 'SHA256:':
                        sha256_value = li.text.split(':')[-1].strip()
                        #print("SHA256:", sha256_value)
                        break
            #print(html_content)
    commits = api.list_repo_commits(model_name)
    com = [commit.commit_id for commit in commits]
    print(com)