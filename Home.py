import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    page_title="NLMyo",
    page_icon="🔧",
)

st.write("# Welcome to NLMyo 🔧")

st.sidebar.success("Select the corresponding tools above.")

st.markdown(
    """

![NLMyo Banner](https://i.imgur.com/avfbQiE.png)

### [NLMyo🔧](https://github.com/lambda-science/NLMyo) is a toolbox built to leverage the power of Large Language Models (LLMs) to exploit histology text reports. 
## How to Use
Select a tool on the left panel to start using NLMyo.  
Here is a sample pdf that you can use with the tools [PDF File](https://www.lbgi.fr/~meyer/IMPatienT/sample_demo_report.pdf)  
Available tools:
- **Anonymizer🕵️**: a simple web-based tool to automatically censor patient histology report PDF.
- **Extract Metadata📝:** a tool to extract metadata from histology reports such as biopsy number, muscle, diagnosis...
- **Auto Classify 🪄:** a tool to automatically predict a diagnosis of congenital myopathy subtype from an histology reports using AI (large language models). Currently can predict between: Nemaline Myopathy, Core Myopathy, Centro-nuclear Myopathy, Non Congenital Myopathy (NON-MC).
- **Report Search 🔎:** a tool to search for a specific term in a set of histology reports. The tool will return the top 5 reports containing closest to your symptom query from our database of reports..

🚨 **DISCLAIMER: This tool use [OpenAI API](https://openai.com/). All data inserted in this tools are sent to OpenAI servers. Please do not upload private or non-anonymized data. As per their terms of service [OpenAI does not retain any data  (for more time than legal requirements, click for source) and do not use them for trainning.](https://openai.com/policies/api-data-usage-policies) However, we do not take any responsibility for any data leak.**

## Contact
Creator and Maintainer: [**Corentin Meyer**, 3rd year PhD Student in the CSTB Team, ICube — CNRS — Unistra](https://lambda-science.github.io/)  <corentin.meyer@etu.unistra.fr>  
The source code for NLMyo is available [HERE](https://github.com/lambda-science/NLMyo)

## Partners

![Partners Banner](https://i.imgur.com/Xk9wBFQ.png)  
MyoQuant is born within the collaboration between the [CSTB Team @ ICube](https://cstb.icube.unistra.fr/en/index.php/Home) led by Julie D. Thompson, the [Morphological Unit of the Institute of Myology of Paris](https://www.institut-myologie.org/en/recherche-2/neuromuscular-investigation-center/morphological-unit/) led by Teresinha Evangelista, the [imagery platform MyoImage of Center of Research in Myology](https://recherche-myologie.fr/technologies/myoimage/) led by Bruno Cadot, [the photonic microscopy platform of the IGMBC](https://www.igbmc.fr/en/plateformes-technologiques/photonic-microscopy) led by Bertrand Vernay and the [Pathophysiology of neuromuscular diseases team @ IGBMC](https://www.igbmc.fr/en/igbmc/a-propos-de-ligbmc/directory/jocelyn-laporte) led by Jocelyn Laporte.  
"""
)

html(
    f"""
    <script defer data-domain="lbgi.fr/nlmyo" src="https://plausible.cmeyer.fr/js/script.js"></script>
    """
)
