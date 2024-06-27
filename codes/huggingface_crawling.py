import requests
from bs4 import BeautifulSoup
import pandas as pd
from huggingface_hub import ModelCard
#from transformers import ModelCard  # Import the transformers library
import time
from unidecode import unidecode
import re
import yaml

MaxPage = 600


def extract_links_from_card(model_card, model_name):
    if model_card and model_card.content:
        model_card_content = model_card.content
        # Define the pattern for GitHub URLs
        url_pattern = r'https?://github\.com/[^\s/$.?#][^\s]*'
        links = re.findall(url_pattern, model_card_content)
        main_github_url = None
        for link in links:
            github_parts = link.split('/')
            if len(github_parts) >= 2:
                # Check if the last part or second-to-last part is in the model_name
                if github_parts[-1] in model_name or github_parts[-2] in model_name:
                    # Remove tree, blob, or any other trailing elements from the GitHub URL
                    remove1 = re.sub(r'[).]+$', '', link)
                    remove2 = re.sub(r'/blob/|/tree/', '/', remove1)
                    remove3 = re.sub(r'/main/', '/', remove2)
                    remove4 = re.sub(r'/examples', '/', remove3)
                    remove5 = re.sub(r'/masters', '/', remove4)
                    remove6 = re.sub(r'/main', '/', remove5)
                    remove7 = re.sub(r'/master', '/', remove6)
                    remove8 = re.sub(r'[),]+$', '', remove7)
                    remove9 = re.sub(r'/models', '/', remove6)
                    github_url = re.sub(r'/(tree|blob)[^/]+', '', remove9)
                    #github_url = re.sub(r'/(tree|blob)[^/]+', '', link)
                    if not main_github_url:
                        main_github_url = github_url
                    if github_url == main_github_url:
                        parts = model_name.split('/')
                        if any(part in github_url for part in parts):
                            model_github_links[model_name] = github_url
                            return github_url
    return None


def get_model_url(model_name):
    return f"https://huggingface.co/{model_name}"


def categorize_pipeline(pipeline_tag):
    # Define the mapping of pipeline tags to categories
    categories = {
        "multimodal": [
            "Feature Extraction",
            "Text-to-Image",
            "Image-to-Text",
            "Text-to-Video",
            "Visual Question Answering",
            "Document Question Answering",
            "Graph Machine Learning"
        ],
        "computer vision": [
            "Depth Estimation",
            "Image Classification",
            "Object Detection",
            "Image Segmentation",
            "Image-to-Image",
            "Unconditional Image Generation",
            "Video Classification",
            "Zero-Shot Image Classification"
        ],
        "natural language processing": [
            "Text Classification",
            "Token Classification",
            "Table Question Answering",
            "Question Answering",
            "Zero-Shot Classification",
            "Translation",
            "Summarization",
            "Conversational",
            "Text Generation",
            "Text2Text Generation",
            "Fill-Mask",
            "Sentence Similarity"
        ],
        "audio": [
            "Text-to-Speech",
            "Text-to-Audio",
            "Automatic Speech Recognition",
            "Audio-to-Audio",
            "Audio Classification",
            "Voice Activity Detection"
        ],
        "tabular": [
            "Tabular Classification",
            "Tabular Regression"
        ],
        "reinforcement learning": [
            "Reinforcement Learning",
            "Robotics"
        ]
    }

    # Convert pipeline_tag to lowercase for case-insensitive matching
    pipeline_tag = pipeline_tag.lower()

    # Iterate through categories and return the category if there's a partial match
    for category, tags in categories.items():
        for tag in tags:
            if tag.lower() in pipeline_tag:
                return category

    # If no partial match is found, return "Other"
    return "Other"


def get_model_card(model_name):
    try:
        model_card = ModelCard.load(model_name)
        return model_card
    except:
        return None

model_github_links = {}


def list_models(task, sort_by):
    total_pages = 0
    models_list = []
    page_number = 11501

    while total_pages < MaxPage:
        url = f"https://huggingface.co/models?pipeline_tag={task}&p={page_number}&sort={sort_by}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content.decode('utf8'), "html.parser")

        for model in soup.find_all('article'):
            try:
                model_name = model.find('a').attrs['href'][1:]
                timestamp = model.find('time').attrs['datetime']
                model_card = ModelCard.load(model_name)
                model_url = get_model_url(model_name)
                model_page = requests.get(model_url)
                model_soup = BeautifulSoup(model_page.content, "html.parser")
                pipeline_tag_element = model_soup.find('a', class_='tag-white')
                if pipeline_tag_element:
                    pipeline_tag = pipeline_tag_element.find('span').text.strip()
                else:
                    pipeline_tag = 'unknown'

                category = categorize_pipeline(pipeline_tag)
                github_lnk = extract_links_from_card(model_card, model_name)
                print(f"{model_name} github is {github_lnk}")


                model_info = {
                    'model_name': model_name,
                    'time_upload': timestamp,
                    'pipeline_tag': pipeline_tag,
                    'category': category,
                    'github_link': github_lnk
                }

                models_list.append(model_info)


            except Exception as e:
                print(f"Error extracting model data: {e}")

        page_number += 1
        print(f'Now printed Page {page_number}')
        total_pages += 1  # Increment the total pages fetched

        time.sleep(5)


    return models_list


task = ""
sort_by = "downloads"
models_list = list_models(task, sort_by)
df = pd.DataFrame(models_list)
df.to_csv('/Users/adekunleajibode/Desktop/crawlingResult/model_name_new_download_11_600.csv', index=False)
#df.to_csv('C:/Experiments/model_name_new_download_pilot.csv', index=False)
print("It is done")