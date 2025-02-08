"""
A class to define the template in order to retrieve data for a figure.
"""

from pydantic import BaseModel, Field

class FigureTemplate(BaseModel):
    """
    A class to define the template for instructions to generate a figure to plot.
    """
    reasoning: str = Field(description="Le raisonnement complet du chatbot pour expliquer pourquoi il a choisi la figure et pourquoi il a choisi les colonnes correspondantes.")
    figure_type: str = Field(description="Le type de figure que le chatbot doit afficher. Les choix possibles sont scatter, line, bar et pie.")
    title: str = Field(description="Le titre de la figure.")
    x_label: str = Field(description="Le nom de la colonne de la table sql correspondant à l'axe des abscisses. Il est important que tu utilises un nom de colonne de la table sql.")
    y_label: str = Field(description="Le nom de la colonne de la table sql correspondant à l'axe des ordonnées. Il est important que tu utilises un nom de colonne de la table sql.")
    color: str = Field(description="La colonne qui permet de colorer les points de la figure. Il est important que tu utilises un nom de colonne de la table sql.")

class FigureInstruction(BaseModel):
    """
    A class to define the template to generate SQL commands to retrieve the date to plot in a figure.
    """
    reasoning: str = Field(description="Le raisonnement complet du chatbot pour répondre à la demande utilisateur et le but de chacune des opérations proposées.'.")
    sql: str = Field(description="Une requête SQLlite qui permet d'obtenir l'information nécessaire pour répondre à la demande utilisateur. Tu utilises SQLlite. Les opérations doivent être que des opérations SQLlite.")
