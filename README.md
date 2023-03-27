![Twitter Follow](https://img.shields.io/twitter/follow/corentinm_py?style=social) ![GitHub last commit](https://img.shields.io/github/last-commit/lambda-science/NLMyo) ![GitHub](https://img.shields.io/github/license/lambda-science/NLMyo)

# NLMyo🔧: a toolbox built to leverage the power of Large Language Models (LLMs) to exploit histology text reports.  

<p align="center">
  <img src="https://i.imgur.com/8yAEAmg.png" alt="NLMyo Banner" style="border-radius: 25px;" />
</p>

**NLMyo🔧: is a toolbox built to leverage the power of Large Language Models (LLMs) to exploit histology text reports.**  
Available tools:
* Anonymizer🕵️: a simple web-based tool to automatically censor patient histology report PDF.
* Extract Metadata📝: a tool to extract metadata from histology reports such as biopsy number, muscle, diagnosis...
* Auto Classify 🪄: a tool to automatically predict a diagnosis of congenital myopathy subtype from an histology reports using AI (large language models). Currently can predict between: Nemaline Myopathy, Core Myopathy, Centro-nuclear Myopathy, Non Congenital Myopathy (NON-MC).
* Report Search 🔎: a tool to search for a specific term in a set of histology reports. The tool will return the top 5 reports containing closest to your symptom query from our database of reports..

🚨 DISCLAIMER: This tool use [OpenAI API](https://openai.com/). All data inserted in this tools are sent to OpenAI servers. Please do not upload private or non-anonymized data. As per their terms of service [OpenAI does not retain any data  (for more time than legal requirements, click for source) and do not use them for trainning.](https://openai.com/policies/api-data-usage-policies) However, we do not take any responsibility for any data leak.

This project is free and open-source under the AGPL license, feel free to fork and contribute to the development.
#### _Warning: This tool is still in early phases and active development._

## How to install
Coming soon  

## How to Use

To use this Streamlit tool, first activate your venv in which NLMyo is installed: `source .venv/bin/activate`  
Then you launch the streamlit server with: `streamlit run Home.py`  

## Contact

Creator and Maintainer: [**Corentin Meyer**, 3rd year PhD Student in the CSTB Team, ICube — CNRS — Unistra](https://cmeyer.fr) <corentin.meyer@etu.unistra.fr>

## Citing MyoQuant🔬

[placeholder]

## Partners

<p align="center">
  <img src="https://i.imgur.com/m5OGthE.png" alt="Partner Banner" style="border-radius: 25px;" />
</p>

NLMyo is born within the collaboration between the [CSTB Team @ ICube](https://cstb.icube.unistra.fr/en/index.php/Home) led by Julie D. Thompson, the [Morphological Unit of the Institute of Myology of Paris](https://www.institut-myologie.org/en/recherche-2/neuromuscular-investigation-center/morphological-unit/) led by Teresinha Evangelista, the [imagery platform MyoImage of Center of Research in Myology](https://recherche-myologie.fr/technologies/myoimage/) led by Bruno Cadot, [the photonic microscopy platform of the IGMBC](https://www.igbmc.fr/en/plateformes-technologiques/photonic-microscopy) led by Bertrand Vernay and the [Pathophysiology of neuromuscular diseases team @ IGBMC](https://www.igbmc.fr/en/igbmc/a-propos-de-ligbmc/directory/jocelyn-laporte) led by Jocelyn Laporte