import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    page_title="NLMyo",
    page_icon="🧰",
)

st.write("# Welcome to NLMyo 🧰")

st.sidebar.success("Select the corresponding tools above.")

st.markdown(
    """

![NLMyo Banner](https://miro.medium.com/v2/resize:fit:1200/0*BKOvjpzn6SPKs81L.png)

[NLMyo🧰 is a toolbox to leverage the power of Large Language Models (LLMs) to exploit histology text reports. ](https://github.com/lambda-science/NLMyo)  

## How to Use

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
