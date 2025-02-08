"""
An object to ask questions to an Azure LLM and interrogate documents in azure AI Search.
"""

from dotenv import load_dotenv
import json
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI
import os

from template.operation_template import OperationInstruction
from template.figure_template import FigureInstruction, FigureTemplate

load_dotenv(override=True)


class LLMClient:
    """
    An object to ask questions to an Azure LLM and interrogate documents in azure AI Search.
    """
    def __init__(self) -> None:
        # OpenAI configuration
        self.OPENAI_API_ENDPOINT = os.environ.get("OPENAI_API_ENDPOINT") 
        self.OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION")
        self.OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
        self.OPENAI_DEPLOYMENT_ID = os.environ.get("OPENAI_DEPLOYMENT_ID")
        self.instruction_template_parser = JsonOutputParser(pydantic_object=OperationInstruction)
        self.figure_instruction_template_parser = JsonOutputParser(pydantic_object=FigureInstruction)
        self.figure_template_parser = JsonOutputParser(pydantic_object=FigureTemplate)
        
        self.LIST_INSTRUCTION_SYSTEM_MESSAGE = SystemMessage(f"""
        Tu es un chatbot qui génère des insights à partir de données utilisateurs. Ton but est de donner une liste d'operations à faire sur les données utilisateurs afin d'obtenir les informations pour répondre à une question utilisateur.
        Tes réponses doivent avoir la forme du json suivant :
        {self.instruction_template_parser.get_format_instructions()}

        **Consigne importante** : Tu ne rajoute rien en dehors de ces deux champs et tu ne retourne que ces deux champs. Il ne faut pas que tu rajoutes d'autres champs.

        Les données à ta disposition sont les suivantes :
            driver_ml (un dataframe qui contient les coefficients associés à chacun des drivers de coûts):
                - driver
                - product (valeurs possibles : Copper, Lead)
                - country (valeurs possibles : US, China)
                - value

            historical_sales_data (un dataframe présentant l'évolution des coûts réels en fonction des produits et des fournisseurs. Ce dataframe donne aussi des prédictions de prix.):
                - product (valeurs possibles : Copper, Lead)
                - date
                - year
                - month (valeurs possibles : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
                - country (valeurs possibles : US, China)
                - provider (valeurs possibles : provider A, provider B, provider C, provider D, provider E, prediction)
                - price
            
            variation_prediction_df (un dataframe qui décompose les prédictions des prix selon plusieurs criteres. Ce dataframe ne contient que les informations sur les predictions.):
                - product (valeurs possibles : Copper, Lead)
                - date
                - year
                - month (valeurs possibles : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
                - country (valeurs possibles : US, China)
                - delta_price (variation des prix des produits)
                - delta_wage (part de la variation des prix dû aux salaires)
                - delta_electrical (part de la variation des prix dû à l'énergie)
                - delta_treatment_price (part de la variation des prix dû au traitement des produits)
                - delta_london_metal_exchange (part de la variation des prix des produits à London Metal Exchange)
                - delta_mechanical (part de la variation des prix dû à la mécanisation)
                - delta_replacement (part de la variation des prix dû au remplacement du matériel par un autre)
                - delta_other (part de la variation des prix d'étiers autres que les precedents)
        
        Ton rôle n'est pas de répondre directement à la question mais de retourner les informations pertinentes pour la prise de décision. Renvoie **TOUTES** les colonnes pertinentes.
        """)
        self.list_instruction_example = "data/instruction_example_conversation.json"

        self.FIGURE_SYSTEM_MESSAGE = SystemMessage(f"""
        Tu es un chatbot qui génère des figures afin d'aider un utilisateur à comprendre sa donnée. Ton but est de donner une liste d'instructions à l'utilisateur afin qu'il comprenne comment obtenir la figure qui répond à sa demande.
        Tes réponses doivent avoir la forme du json suivant :
        {self.figure_instruction_template_parser.get_format_instructions()}
        
        **Consigne importante** : Tu ne rajoute rien en dehors de ces deux champs et tu ne retourne que ces deux champs.
        **Consigne importante** : Si on te demande de concaténer les valeurs de deux colonnes, fait colonne_a || " " || colonne_b.

        Les données à ta disposition sont les suivantes :
            driver_ml (un dataframe qui contient les coefficients associés à chacun des drivers de coûts):
                - driver
                - product (valeurs possibles : Copper, Lead)
                - country (valeurs possibles : US, China)
                - value

            historical_sales_data (un dataframe présentant l'évolution des coûts réels en fonction des produits et des fournisseurs. Ce dataframe donne aussi des prédictions de prix.):
                - product (valeurs possibles : Copper, Lead)
                - date
                - year
                - month (valeurs possibles : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
                - country (valeurs possibles : US, China)
                - provider (valeurs possibles : provider A, provider B, provider C, provider D, provider E, prediction)
                - price
            
            variation_prediction_df (un dataframe qui décompose les prédictions des prix selon plusieurs criteres. Ce dataframe ne contient que les informations sur les predictions.):
                - product (valeurs possibles : Copper, Lead)
                - date
                - year
                - month (valeurs possibles : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
                - country (valeurs possibles : US, China)
                - delta_price (variation des prix des produits)
                - delta_wage (part de la variation des prix dû aux salaires)
                - delta_electrical (part de la variation des prix dû à l'énergie)
                - delta_treatment_price (part de la variation des prix dû au traitement des produits)
                - delta_london_metal_exchange (part de la variation des prix des produits à London Metal Exchange)
                - delta_mechanical (part de la variation des prix dû à la mécanisation)
                - delta_replacement (part de la variation des prix dû au remplacement du matériel par un autre)
                - delta_other (part de la variation des prix d'étiers autres que les precedents)
        
        Ton rôle n'est pas de répondre directement à la question mais de retourner les informations pertinentes pour la prise de décision. Renvoie **TOUTES** les colonnes pertinentes.
            """)
        self.figure_example = "data/plot_figure_example_conversation.json"

        self.llm = AzureChatOpenAI(
            azure_endpoint=self.OPENAI_API_ENDPOINT,
            openai_api_key=self.OPENAI_API_KEY,
            api_version=self.OPENAI_API_VERSION,
            azure_deployment=self.OPENAI_DEPLOYMENT_ID,
            temperature=0,
            top_p = 0,
            max_tokens=2048,
            seed=42
            )

        # Initialize the message history.
        self.messages = []

    def load_example_conversation(self, address):
        """
        Loads a file of an example conversation in order to do few shot learning.

        no input

        no output
        """
        self.clear_chat_memory()
        with open(address, "r") as f:
            all_messages = json.load(f)
        for message in all_messages:
            self.add_message_to_history(role = message["role"], content = message["content"])

    def add_message_to_history(self, role, content):
        """
        Add a message to the chat history with the role of the person who wrote the message and its content
        
        input:
            role (str)
            message (str)
            
        no output 
        """
        if role == "user":
            self.messages.append(HumanMessage(content = content))
        if role == "assistant":
            self.messages.append(AIMessage(content = str(content)))
        
    def clear_chat_memory(self):
        """
        Clear chat history and resets conversation
        
        no input
            
        no output 
        """
        self.messages = []
    
    def get_message_history(self):
        """
        Returns the message history

        no input

        output:
            message_list (list)
        """
        return self.messages
    
    def get_interpretation(self, prompt, full_response, table):
        """
        Method to ask a question to an LLM when we want an interpretation of the answer.

        input:
            prompt (str)
            full_response (str)
            table (str)
            
        output:
            (str)
            
        """
        instruction_prompt = f"""
        Tu es un chatbot d'aide à l'analyse et à la décision. Un utilisateur a posé la question suivante : {prompt}. 
        Afin de répondre à cette question, tu as proposé la démarche suivante : {full_response['reasoning']} et tu as executé sur ta base de donnée la requête SQL suivante : {full_response['sql']}.
        La requête a donné la table suivante : {table}.

        Tu veux avoir les prix les plus bas possibles sur les produits et tu donnes des conseils aux utilisateurs pour choisir la meilleure période et le meilleur fournisseur pour cela.
        En utilisant ces informations et en expliquant tes raisonnements, réponds à la question utilisateur.
        Tes réponses sont courtes, claires et précises.
        """
        # We send the request
        llm_response = self.llm.invoke([{"role": "user", "content": instruction_prompt}])
        return llm_response.content

    def get_operation_figure(self, user_query):
        """
        Method to ask a question to an LLM when we want as output a list of operations to do on data.

        input:
            prompt (str)
            
        output:
            (str)
            
        """
        self.load_example_conversation(self.list_instruction_example)
        chat_template = ChatPromptTemplate.from_messages([self.FIGURE_SYSTEM_MESSAGE, MessagesPlaceholder(variable_name="messages")])
        chain = chat_template | self.llm | self.figure_instruction_template_parser

        response = chain.invoke({"messages": self.messages + [HumanMessage(content = user_query)]})
        return response
    
    def get_figure_template(self, prompt, full_response):
        """
        Method to ask a question to an LLM when we want as output a list of operations to do on data.

        input:
            prompt (str)
            
        output:
            (str)
            
        """
        self.load_example_conversation(self.figure_example)
        chat_template = ChatPromptTemplate.from_messages([MessagesPlaceholder(variable_name="messages")])
        user_message_reworked = f"""Tu es un chatbot d'aide à la création de figures. Un utilisateur a fait la demande suivante : {prompt}. 
            Afin de répondre à cette question, tu as proposé la démarche suivante : {full_response['reasoning']} et tu as executé sur ta base de donnée la requête SQL suivante : {full_response['sql']}.
            **Instruction importante** : Il est **très important** que tu utilises les noms de colonnes de la table sql. Respecte les noms de colonnes de la table sql et la casse des noms.
            Il faut maintenant tracer une figure qui permet de répondre à la demande de l'utilisateur.
            Ta réponse doit répondre en suivant ce template : {self.figure_template_parser.get_format_instructions()}.
            """
        #print(figure_prompt.format(prompt = prompt))
        chain = chat_template | self.llm | self.figure_template_parser

        response = chain.invoke({"messages": self.messages + [HumanMessage(content = user_message_reworked)]})
        return response

    def get_list_operation(self, user_query):
        """
        Method to ask a question to an LLM when we want as output a list of operations to do on data.

        input:
            prompt (str)
            
        output:
            (str)
            
        """
        self.load_example_conversation(self.list_instruction_example)
        chat_template = ChatPromptTemplate.from_messages([self.LIST_INSTRUCTION_SYSTEM_MESSAGE, MessagesPlaceholder(variable_name="messages")])
        chain = chat_template | self.llm | self.instruction_template_parser

        response = chain.invoke({"messages": self.messages + [HumanMessage(content = user_query)]})
        return response
