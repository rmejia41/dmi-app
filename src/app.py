
import pandas as pd
import plotly.express as px  
import dash
from dash import Dash, dcc, html, Input, Output, State  

app = dash.Dash(__name__)
server = app.server

df = pd.read_csv("https://github.com/rmejia41/first-google-app/raw/main/dmi.csv")

# App layout
app.layout = html.Div([

    html.H1("Web Application: CDC Funding for the Data Modernization Initiative (DMI)", style={'text-align': 'center'}),

    dcc.Dropdown(id="Population Categories",
                 options=[
                     {"label": "< 20 Millions", "value": 1},
                     {"label": "20-60 Millions", "value": 2},
                     {"label": "60 - 100 Millions", "value": 3},
                     {"label": "> 100 Millions", "value": 4}],
                 multi=False,
                 value=1,
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_dmi_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_dmi_map', component_property='figure')],
    [Input(component_id='Population Categories', component_property='value')]
)
def update_graph(option_cat):
    print(option_cat)
    print(type(option_cat))

    container = "The funding category chosen by user was: {}".format(option_cat)

    dff = df.copy()
    dff = dff[dff["Population Categories"] == option_cat]

    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='Jurisdiction',
        scope="usa",
        color='Total CDC/DMI Funding ($)',
        hover_data=['Jurisdiction', 'Total CDC/DMI Funding ($)'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'DMI Funding ($)': 'Total Funding ($)'},
        template='plotly_dark'
    )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)