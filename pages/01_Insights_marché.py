"""
Streamlit interface for the page to generate insights using generative AI.
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

intro_sentence = "Je connais l'évolution des prix du marché pour vos fournisseurs. Posez-moi toutes vos questions, je serai enchanté d'y répondre 😃."

st.session_state['interface_client'].configure_page()
st.title("Generation d'insights")

st.session_state['interface_client'].create_sidebar(
    header_text = "Génération dynamique d'insights s'appuyant sur vos données",
    paragraph_text = "Le chatbot effectue des recherches sur vos données afin de pouvoir fournir des insights et des recommandations.",
    clear_conversation_button=True)

# Display past conversation history
st.session_state['interface_client'].display_message_history()

full_response = ""
table_answer = ""
# Capture user prompt and store in session state
if prompt := st.chat_input("Comment puis-je vous aider ?"):
    st.session_state['interface_client'].add_message_to_history("user", prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    # Placeholder for assistant response with initial empty string
    try:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = st.session_state['llm_client'].get_list_operation(prompt)
            print(full_response)
            table_answer = st.session_state['operation_client'].read_operation(full_response["sql"])
            llm_interpretation = st.session_state['llm_client'].get_interpretation(prompt, full_response, pd.DataFrame(table_answer).to_markdown())

            clean_answer = st.session_state['interface_client'].format_answer_for_history(full_response["reasoning"], table_answer, llm_interpretation)
            # Update placeholder with complete cleaned response
            message_placeholder.markdown(clean_answer)

        # Lines to add previous questions to chat history. (Having too large a chat history can degrade performances)
        #st.session_state['llm_client'].add_message_to_history("user", prompt)
        #st.session_state['llm_client'].add_message_to_history("assistant", full_response)
        # Append assistant response to session state
        st.session_state['interface_client'].add_message_to_history("assistant", clean_answer)
    except Exception as e:
        print(e)
        full_response = "Je suis désolé, je n'arrive pas à répondre à votre question. Pourriez-vous essayer de reformuler ?"
        message_placeholder.markdown(full_response)
        st.session_state['interface_client'].add_message_to_history("assistant", full_response)

# Display intro sentence
st.session_state['interface_client'].display_intro_sentence(intro_sentence)
