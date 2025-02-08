"""
A class to define the template for a list of instruction to do in order to transform data into insights.
"""

from pydantic import BaseModel, Field

class OperationInstruction(BaseModel):
    """
    A class to define the template for a list of instruction to do in order to transform data into insights.
    """
    reasoning: str = Field(description="Le raisonnement complet du chatbot pour répondre à la demande utilisateur et le but de chacune des opérations proposées. Par exemple : 'Afin de trouver chez quel fournisseur acheter du cuivre en 2025, il faut trouver le prix moyen du cuivre de chacun des fournisseurs en 2025 et choisir le prix le plus bas'.")
    sql: str = Field(description="Une requête SQLlite qui permet d'obtenir l'information nécessaire pour répondre à la demande utilisateur. Tu utilises SQLlite. Les opérations doivent être que des opérations SQLlite.")
