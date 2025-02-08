"""
An interface client which standardizes how the application is supposed to look like.
"""

import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import time


class InterfaceClient:
    """
    An interface client which standardizes how the application is supposed to look like.
    """
    def __init__(self) -> None:
        self.logo = Image.open('images/logo.png')
        self.large_logo = Image.open('images/logo-wide.png')
        self.title = "Query your data"
        self.display_history = []

    def add_message_to_history(self, role, content):
        """
        Method to add a message to the list of messages to display on screen
        NOTE : This doesn't mean the message will be taken in account by the LLM.
        input:
            role (str) valeurs possibles : assistant et user
            content (str)

        no output
        """
        self.display_history.append({"role": role, "content": content})

    def configure_page(self, page_title="Query your Data"):
        """
        Method to configure our page (name, logo, etc.)

        input:
            page_title (str)

        no output
        """
        st.set_page_config(page_title=page_title, page_icon=self.logo, layout="centered", initial_sidebar_state="auto", menu_items=None)

    def create_sidebar(self, header_text=None, paragraph_text="", clear_conversation_button=False):
        """
        Create a sidebar with text and a reset conversation button.

        input:
            header_text (str)
            paragraph_text (str)
            clear_conversation_button (bool)

        no output
        """
        with st.sidebar:
            # Display logo image
            st.sidebar.image(self.large_logo)
            if header_text is not None:
                with st.container():  
                    self.display_markdown_in_container(st, header_text, paragraph_text)
                 # Add space using markdown for consistency  
                st.sidebar.markdown("<hr style='border-top: 1px solid #000000;'>", unsafe_allow_html=True)  
                with st.container(): self.display_markdown_in_container(st, "", "")
                with st.container(): self.display_markdown_in_container(st, "", "")
            if clear_conversation_button:
                with stylable_container(
                    key="clear_memory",
                    css_styles="""
                        button {
                            background-color: #5723F3;
                            color: #ffffff;
                            border-radius: 42px;
                            cursor:pointer;
                        }
                    """,
                ):
                    if st.button("Effacer la conversation →"):
                        self.display_history = []

    def display_intro_sentence(self, intro_sentence):
        """
        Displays an intro sentence to greet users using the chat messages

        input:
            intro_sentence (str)

        no output
        """
        if self.display_history == []:
            message_placeholder = st.empty()
            streamed_content = ""
            for splitted_content in intro_sentence.split(" "):
                streamed_content = streamed_content + " " + splitted_content 
                message_placeholder.markdown(streamed_content)
                time.sleep(0.07)
            message_placeholder.markdown(intro_sentence)

    def display_markdown_in_container(self, container, header_text, paragraph_text):
        """
        Displays markdown-styled text in a container

        input:
            container (streamlit object)
            header_text (str)
            paragraph_text (str)
        
        no output

        """
        container.markdown(f"<h3 style='color: #000000;'>{header_text}</h3>", unsafe_allow_html=True)  
        container.markdown(f"<p style='color: #000000;'>{paragraph_text}</p>", unsafe_allow_html=True)
    
    def display_message_history(self):
        """
        Displays past messages.

        no input
        no output
        """
        # Display past conversation history
        for message in self.display_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def format_answer_for_history(self, reasoning, table, interpretation):
        """
        Decomposes an LLM message in order to print it in our message history correctly

        input:
            reasoning (str)
            table (str)
            interpretation (str)

        output:
            str
        """
        answer = f"""
**Raisonnement** : {self.replace_malformed_characters(reasoning)}

---

**Données** : 

{pd.DataFrame(table).to_markdown()}

---

**Conclusion** : {self.replace_malformed_characters(interpretation)}
    """
        return answer
    
    def replace_malformed_characters(self, text):
        """
        Replace malformed characters in text

        input:
            text (str)

        output:
            str
        """
        return text.replace("Ã©", "é").replace("Ã", "à").replace("Ã¨", "è").replace("àª", "ê")