Contact : clement.lionceau@gmail.com

last modification date : 30/10/2024

# Query Data Table

## Objective

This application is a chatbot to ask for insights on your data bases and to create visualizations in order to understand a database.
The application has a streamlit interface.

## Content

This github contains the following files and folders :
- .streamlit (folder)
    - config.toml (information for visual configuration)
- helper (folder)
    - authentication_client.py (takes care of authentication of users. Currently unused)
    - interface_client.py (takes care of displaying the interface)
    - LLM_client.py (takes care of the generative AI part)
    - operation_client.py (takes care of data transformation)
- images (folder)
    - methodologie.png
    - logo.png
    - logo-wide.png
- pages (folder used by streamlit to generate navigation)
    - 01_insights_marche.py (takes care of insight generation)
    - 03_Generation_figures.py (takes care of visualization generation)
- template (folder)
    - figure_template.py (format for generative AI answers for plotly figure generation)
    - operation_template.py (format for generative AI answers for SQL operation generation)
- Main_menu.py (file to launch the streamlit application)
- README.md 
- requirements.txt (probably not up to date)

## Data

The application plots insights on data. In order to do so, you must add a data folder with the files you want to work on. Depending on the form of the files you have, you will have to adapt your LLM prompts.

As an example, you will find underneath the csv and json files used in our case :
- driver_importance.csv (separator : ";") (The specified columns and values are specified in the prompts of the LLM_client.py file)
- historical_sales_data.csv (separator : ";") (The specified columns and values are specified in the prompts of the LLM_client.py file)
- instruction_example_conversation.json (an example quqestion + answer for our LLM model in order for him to generate SQL instructions)
- plot_figure_example_conversation.json (an example quqestion + answer for our LLM model in order for him to generate plotly figures)


## Run the project

In order to run the project, you need to add a .env file in your main directiry with the following fields :
- OPENAI_API_KEY
- OPENAI_API_ENDPOINT
- OPENAI_API_VERSION
- OPENAI_DEPLOYMENT_ID 

In order to launch the application, go in the main folder and run the command :
```python
streamlit run Main_menu.py
```

Exemples de questions qui fonctionnent

PoC 1 : travail des données
1) Je suis en octobre 2024. Mon fournisseur de cuivre me propose un prix de 6000. Est-ce que je devrais acheter chez lui ou chez un autre fournisseur ?
2) D'après les prédictions, quel sera le meilleur mois pour acheter du plomb en 2025 et dans quel pays ?
3) Nous sommes en 2024. Est-ce que je devrais faire du stock de cuivre cette année ou est-ce que je devrais acheter l'année prochaine ?
4) Je suis en octobre 2024. J'ai envie d'acheter du cuivre, est-ce que je le fais maintenant ou est-ce que j'attends quelques mois ? Utilise les derniers mois d'avant pour justifier ta réponse.

Nous sommes en Octobre 2024. Sur les six derniers mois, sommes-nous sur une tendance à la hausse pour le plomb ?
5) En utilisant les drivers, comment expliquer le hausse du prix du cuivre en 2025 ?

PoC 2 : tracé de figures
- Trace l'évolution du prix du cuivre au cours du temps. Sépare les fournisseurs et inclut les prédictions.
- pour les drivers de couts du cuivre aux US, tu peux me tracer un camembert qui m'indique leur importance (en valeur absolue) à chacun ?
- Pour chaque fournisseur de plomb, donne moi un bar chart qui présente la moyenne des prix pour chaque année entre 2023 et 2025
- Quelle est l'évolution du prix du cuivre au cours du temps en 2024 et 2025 pour le fournisseur A trace aussi les données de prédictions pour le cuivre aux US.


## Image credits

Looking glass icon image : <a href="https://www.flaticon.com/free-icons/research" title="research icons">Research icons created by ibrandify - Flaticon</a>

## Contribute

