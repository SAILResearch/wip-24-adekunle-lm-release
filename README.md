# The Traits and Characteristics of Pre-trained Language Model Releases on HuggingFace: An Exploratory Analysis
Recently, WhatsApp and Facebook have integrated Meta AI, built upon their latest and most advanced technology, Llama-3, into their applications. This allows users to leverage Meta AI for various tasks.
These advanced technologies are called pre-trained models. Many pre-trained models exist for different tasks, including Natural Language Processing (NLP), computer vision, and audio processing. The most common application of these technologies is large language processing (LLP), a subfield of NLP that focuses on enabling machines to understand,interpret, and generate human language. Pre-trained language models (PTLMs) are specifically designed for comprehending human language.
PTLMs vary in size, with parameter counts ranging from thousands to billions. Models with over 1 million parameters are classified as pre-trained large language models (PTLLMs), such as Llama, GPT, BERT, T5, and RoBERTa.
The good news is that many of these models are accessible through downstream model registries, allowing developers and users to leverage PTLLMs in their applications. Several registries offer free access to pre-trained models for various downstream tasks, including Hugging Face (HF), ONNX, PyTorch, and Modelhub. Hugging Face is the largest of these,boasting over 650,000 pre-trained models. Exploring practices on this registry is valuable.
However, selecting the appropriate PTLLM for specific applications can be challenging. Users face various hurdles, such as:
- Search terms: How to find the most suitable model?
- Variants: Which variant of PTLLM is available and recommended?
- Versions: What versions are available?
Unfortunately, no current documentation informs users about the types of variants model developers push to Hugging Face, the naming conventions for PTLLMs, or versioning practices. The AI community has yet to address these issues.
Therefore, it's crucial to explore the current naming conventions, versioning practices, and available variants of PTLLMs and their characteristics. Similarly, it's important to understand if the versioning conventions on Hugging Face align with those used in software development.
We employed a mixed-methods approach (quantitative and qualitative analysis) to make observations, which are discussed below.

## Naming and Versioning practices on HuggingFace
On HuggingFace, approximately 149 different naming conventions are observed, indicating a significant level of inconsistency across repositories. This discrepancy may stem from a mismatch between user preferences and practical naming practices for PTLLMs. Moreover, 13 key terms frequently appear in PTLLM names, including identifiers, base models, parameter sizes, training mechanisms, descriptions, variant types, versions, tasks, datasets, targeted languages, development dates, owning nationalities, and some ambiguous terms.

Regarding versioning, two main types of identifiers are used: major (e.g., v1, v2) and minor (e.g., v1.x, v2.x), with major identifiers being more common. Additionally, files associated with PTLLM releases undergo frequent changes, with over 192 different file types identified across repositories. These files are categorized into five groups: Code files, Documentation files, Data and Configuration files, Model files, and Other files. The most frequently changed files are model binary files and data & configuration files.

Furthermore, there are 11 different file extensions associated with PTLLMs on HuggingFace, including .safetensor, .bin, .pt, .model, .onnx, .meta, .tflite, .mlmodel, .ckpt, .mdl, and .pb. Notably, .safetensor is the most prevalent extension, potentially indicating a community shift towards secure and efficient storage solutions.

## PTLLMs provenance, variant types and their characteristics on HF
In evaluating PTLLMs on HuggingFace, we've noted a focus on transparency and reproducibility. Many PTLLMs are released with their configuration files, indicating an effort towards reproducible model training configurations. Since 2022, 299 PTLLMs have been released on HF, with Gemma, Mistral, Llama, Bert, and Mixtral being the most prevalent models. However, only 24% of these models include information about their training datasets in their repositories.

Model developers on HF employ 15 different keywords, such as ft, deduped, and distilled, to denote variant types. These keywords are classified into four groups: Fine-tuning, Deduplication, Quantization, and Knowledge Distillation. Fine-tuned models emerge as the most prevalent, but a significant portion of released models do not specify their variant type.

Concerningly, only a small percentage of variant models include their training datasets in their repositories—22% for Fine-tuned models, 23% for Quantized models, 25% for Deduped models, and 36% for Distilled models. This transparency gap may impede user comprehension.

In terms of transparency, we found that 67% of released PTLLMs on HF have model cards—a significant increase compared to previous literature findings of 7%. However, there is a notable disparity in model card release among variant types, with Deduped models exhibiting particularly low release rates at 31%. There are statistically significant differences between the release of model cards and the variant types of a model.

## Changes that lead to versioning of PTLLMs on HF.
We explored the versioning practices of PTLLMs on HuggingFace to understand the changes leading to new versions. Developers use major and minor identifiers similar to those in software engineering. Our analysis revealed that only 43% of major versions and 35% of minor versions have their predecessors available, indicating poor versioning practices.
We found that changes to PTLLMs for new versions include modifications to base models, binary files, binary file pointers, README documents, and model cards. Statistically significant changes were observed only in model binary files and base models, suggesting these are key differentiators for new versions.
Further examination of README and model cards for versions with changes in model weight files revealed 31 different changes between major versions and 10 between minor versions. Interestingly, all minor version changes also appeared in major versions. We categorized these changes into nine groups: configuration change, model architecture change, license change, performance change, dataset change, training library change, energy consumption change, evaluation metric change, and other changes. However, there was no statistical significance between changes in major and minor versions, suggesting arbitrary use of these identifiers by developers.
Lastly, we discovered that changes in configuration settings, training libraries, and evaluation metrics are associated with model performance improvements. This implies that altering these aspects can enhance the performance of new PTLLM versions.

## The folders
- dataset_folder: This folder contain all the dataset used for the analysis in this study.
- RQ1_results: This folder contains the graphs and the randomly selected candidates for the manual analysis we condicted in this study for RQ1
- RQ2_result: This folder also contain the graphs and some other related information.
- RQ3_result: This folder also contain the figure and the randomly sampled candidate for the manual analysis we performed in this study.
- The .py and .ipynb files: These files contain the codes for the result analysis.

## Requirements
- Python programming language
- Python libraries:
  *  Beautifulsoup
  *  Requests
  *  Pandas
  *  Huggingface_hub
  *  Numpy
  *  Seaborn
  *  Matplotlib

## Authors
- Ajibode Adekunle
- Abdul Ali Bangash
- Filipe Roseiro Cogo
- Bram Adams
- Ahmed E. Hassan
