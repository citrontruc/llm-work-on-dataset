"""
Main file from which to run all operations
"""

import streamlit as st

from helper.interface_client import InterfaceClient


if 'interface_client' not in st.session_state:
    st.session_state['interface_client'] = InterfaceClient()

def main():
    """
    Main method to coordinate all our operations using our clients.
    """
    st.session_state['interface_client'].configure_page()
    # Insert explanation for the use case and a data model to show
    st.title("Prédictions des prix de matériaux")
    st.header("Compréhension des facteurs de ventes et prédictions des prix.")
    st.image("images/methodologie.png")
    st.markdown("Le but de cette application est de fournir des insights à l'utilisateur afin de pouvoir l'aider à déterminer le moment opportun afin d'acheter des matériaux dont les prix varient en fonction du temps et par fournisseurs.  \n"
                "Dans le cadre de l'étude, l'historique des prix a été étudié et a permis de déterminer un modèle de coûts avec plusieurs drivers. En utilisant les variations des drivers de coûts et l'historique des prix, des prédictions sont faites par **machine learning**.  \n"
                "Cette application permet de générer des insights et des recommandations en s'appuyant sur les données historiques. Elle permet aussi de générer des visualisations supplémentaires si on souhaite étudier un aspect en particulier.")
    
    st.session_state['interface_client'].create_sidebar()

if __name__ == "__main__":
    main()
