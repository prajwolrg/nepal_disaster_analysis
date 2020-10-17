import pandas as pd
import json

import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.express as px

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


df = pd.read_excel("disaster_data.xlsx", skiprows=5, usecols="A:AA", parse_dates=True)
df["Incident Date"] = pd.to_datetime(df["Incident Date"], errors="coerce")

damage_measures = [
    "Death Male",
    "Death Female",
    "Death Unknown",
    "Total Death",
    "Missing People",
    "Affected Family",
    "Estimated Loss",
    "Injured",
    "Govt. Houses Fully Damaged",
    "Govt. Houses Partially Damaged",
    "Private House Fully Damaged",
    "Private House Partially Damaged",
    "Displaced Male(N/A)",
    "Displaced Female(N/A)",
    "Property Loss",
    "No. of Displaced Family",
    "Cattles Loss",
    "Displaced Shed",
]

app = dash.Dash()

app.layout = html.Div(
    children=[
        html.H1("Hello world"),
        dcc.Dropdown(
            id="damage",
            options=[
                {"label": measure, "value": measure} for measure in damage_measures
            ],
            value="Total Death",
        ),
        dcc.Graph(id="bar_plot"),
        dcc.Graph(id="line_chart"),
        html.Pre(id="hoverdata"),
    ]
)


@app.callback(Output("bar_plot", "figure"), [Input("damage", "value")])
def generate_bar_plot(damage):
    damage_sum = (df.groupby("Incident")[damage].sum()).reset_index()
    damage_sum = damage_sum.sort_values(damage, ascending=False)
    fig = px.bar(damage_sum, x="Incident", y=damage)
    return fig


@app.callback(
    Output("line_chart", "figure"),
    [Input("damage", "value"), Input("bar_plot", "clickData")],
)
def generate_line_chart(damage, clickData):
    incident = clickData["points"][0]["x"]
    incident_df = df[df["Incident"] == incident]
    incident_df = incident_df.set_index("Incident Date")
    incident_df = incident_df[[damage]].resample("m").sum()
    incident_df = incident_df.reset_index()

    fig = px.line(incident_df, x="Incident Date", y=damage)

    return fig


if __name__ == "__main__":
    app.run_server()
