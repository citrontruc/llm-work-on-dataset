"""
A class to compute operations on data.
"""
from colour import Color
import pandas as pd
from pandasql import sqldf
import plotly.express as px
import plotly.graph_objects as go


class OperationClient:
    """
    A class to compute operations on data.
    """
    def __init__(self):
        self.list_table_name = ["driver_ml", "historical_sales_data", "variation_prediction_df"]
        self.table_dict = {}
        for table_name in self.list_table_name:
            self.table_dict[table_name] = pd.read_csv(f"data/{table_name}.csv", sep=";")

    def read_operation(self, sql_operation):
        """
        Given a list of operations and their input parameters, returns the output of the last operation.

        input:
            list_operations (str)

        output:
            (pd.DataFrame)
        """
        result = sqldf(sql_operation, self.table_dict)
        return result
    
    def plot_figure(self, sql_operation, figure_instruction):
        """
        Given a list of operations and their input parameters, returns the output of the last operation.

        input:
            list_operations (str)
            figure_instruction (dict)

        output:
            (plotly figure)
        """
        result = pd.DataFrame(sqldf(sql_operation, self.table_dict))

        match figure_instruction["figure_type"]:
            case "bar":
                plotly_fig = getattr(px, figure_instruction["figure_type"])(result, x=figure_instruction["x_label"].lower(), y=figure_instruction["y_label"].lower(), title=figure_instruction["title"], color=figure_instruction["color"].lower(), barmode="group", text_auto=True)
            case "histogram":
                plotly_fig = getattr(px, figure_instruction["figure_type"])(result, x=figure_instruction["x_label"].lower(), y=figure_instruction["y_label"].lower(), title=figure_instruction["title"], color=figure_instruction["color"].lower(), barmode="group", text_auto=True)
            case "scatter":
                plotly_fig = getattr(px, figure_instruction["figure_type"])(result, x=figure_instruction["x_label"].lower(), y=figure_instruction["y_label"].lower(), title=figure_instruction["title"], color=figure_instruction["color"].lower(), symbol=figure_instruction["color"])
                # Part of code used to get more beautiful colors for scatterplots
                #blue = Color("blue")
                #unique_value = result[figure_instruction["color"]].unique()
                #colors = list(blue.range_to(Color("red"), len(unique_value)))
                #dict_color = {}
                #for i in range(len(unique_value)):
                #    dict_color[unique_value[i]] = colors[i].hex_l
                #plotly_fig = go.Figure()
                #plotly_fig.add_trace(go.Scatter(x = result[figure_instruction["x_label"].lower()], y = result[figure_instruction["y_label"].lower()], mode = 'lines+markers', marker_color = [dict_color[element] for element in result[figure_instruction["color"].lower()].values]))
                #plotly_fig.update_layout(title=figure_instruction["title"], xaxis_title=figure_instruction["x_label"], yaxis_title=figure_instruction["y_label"])
            case "pie":
                plotly_fig = getattr(px, figure_instruction["figure_type"])(result, names=figure_instruction["x_label"].lower(), values=figure_instruction["y_label"].lower(), title=figure_instruction["title"], color=figure_instruction["color"].lower())
            case "line":
                plotly_fig = getattr(px, figure_instruction["figure_type"])(result, x=figure_instruction["x_label"].lower(), y=figure_instruction["y_label"].lower(), title=figure_instruction["title"], color=figure_instruction["color"].lower(), markers = False)
            case _:
                plotly_fig = getattr(px, figure_instruction["figure_type"])(result, x=figure_instruction["x_label"].lower(), y=figure_instruction["y_label"].lower(), title=figure_instruction["title"], color=figure_instruction["color"].lower())
        return plotly_fig
