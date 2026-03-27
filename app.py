import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

# Create app
app = dash.Dash(__name__)

# Dark theme style
app.layout = html.Div(style={'backgroundColor': '#0d1117', 'color': 'white', 'padding': '20px'}, children=[

    html.H1("Global Economic Shock Simulator", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Oil Price"),
        dcc.Slider(20, 150, step=1, value=70, id='oil-slider'),

        html.Label("Inflation Rate (%)"),
        dcc.Slider(0, 15, step=0.5, value=5, id='inflation-slider'),

        html.Label("Risk Level"),
        dcc.Slider(1, 10, step=1, value=3, id='risk-slider'),

        html.Label("Trade Index"),
        dcc.Slider(80, 130, step=1, value=100, id='trade-slider'),
    ], style={'marginBottom': '40px'}),

    dcc.Graph(id='economic-graph'),

    html.Div(id='output-text', style={'fontSize': 20, 'marginTop': '20px'})
])

# Model function
def economic_model(oil, inflation, risk, trade):
    gdp = 2.5 + 0.03*oil - 0.5*inflation + 0.02*trade - 0.4*risk
    stability = 100 - (risk*5 + inflation*2)
    return gdp, stability

# Callback
@app.callback(
    [Output('economic-graph', 'figure'),
     Output('output-text', 'children')],
    [Input('oil-slider', 'value'),
     Input('inflation-slider', 'value'),
     Input('risk-slider', 'value'),
     Input('trade-slider', 'value')]
)
def update_graph(oil, inflation, risk, trade):

    years = np.arange(2020, 2030)
    gdp_values = []
    
    for year in years:
        gdp, stability = economic_model(oil, inflation, risk, trade)
        gdp_values.append(gdp)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=years,
        y=gdp_values,
        mode='lines+markers',
        line=dict(color='cyan', width=3),
        name='GDP Projection'
    ))

    fig.update_layout(
        title="GDP Projection Under Economic Shock",
        plot_bgcolor='#0d1117',
        paper_bgcolor='#0d1117',
        font=dict(color='white')
    )

    gdp, stability = economic_model(oil, inflation, risk, trade)

    text = f"Predicted GDP Growth: {gdp:.2f}% | Stability Index: {stability:.2f}"

    return fig, text


if __name__ == '__main__':
    app.run(debug=True)
