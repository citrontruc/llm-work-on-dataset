"""
Streamlit interface for the page to generate figures using generative AI.
"""

import pandas as pd
import streamlit as st

from helper.interface_client import InterfaceClient
from helper.LLM_client import LLMClient
from helper.operation_client import OperationClient

if 'llm_client' not in st.session_state:
    st.session_state['llm_client'] = LLMClient()

if 'operation_client' not in st.session_state:
    st.session_state['operation_client'] = OperationClient()

if 'interface_client' not in st.session_state:
    st.session_state['interface_client'] = InterfaceClient()

intro_sentence = "Je peux tracer des figures afin de pouvoir vous aider à mieux visualiser l'information. Posez-moi toutes vos questions, je serai enchanté d'y répondre 😃."

st.session_state['interface_client'].configure_page()
st.title("Generation de visualisations")

st.session_state['interface_client'].create_sidebar(
    header_text = "Génération dynamique de figures s'appuyant sur vos données",
    paragraph_text = "Le chatbot essaie de trouver une visualisation pertinente de vos données afin de répondre à vos questions.",
    clear_conversation_button=True)

full_response = ""
table_answer = ""
# Capture user prompt and store in session state
if prompt := st.chat_input("Comment puis-je vous aider ?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    # Placeholder for assistant response with initial empty string
    try:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = st.session_state['llm_client'].get_operation_figure(prompt)
            print("full_response", full_response)
            figure_answer = st.session_state['llm_client'].get_figure_template(prompt, full_response)
            print("figure_answer", figure_answer)
            plotly_figure = st.session_state["operation_client"].plot_figure(full_response["sql"], figure_answer)

            # Update placeholder with plotly chart
            message_placeholder.plotly_chart(plotly_figure, use_container_width=True)

    except Exception as e:
        print(e)
        full_response = "Je suis désolé, je n'arrive pas à répondre à votre question. Pourriez-vous essayer de reformuler ?"
        message_placeholder.markdown(full_response)
