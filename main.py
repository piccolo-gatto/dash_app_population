from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash()

labels = {'lifeExp': 'life experience', 'pop': 'population', 'gdpPercap': 'gdp'}
app.layout = html.Div([
    html.H1(children='World population', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
            dcc.Dropdown(df['country'].unique(), [df.country.unique()[0]], multi=True, id='country-val'),
            dcc.Dropdown(labels, list(labels.keys())[1], id='line-y-value')],
            style={'display': 'flex', 'flexDirection': 'column', 'width': '30%', 'height': '10%'}),

        dcc.Graph(id='line-graph', style={'width': '70%', 'height': '10%'})],
        style={'display': 'flex', 'flexDirection': 'row', 'height': '10%'}),
    html.Div([
        dcc.Dropdown(df['year'].unique(), df['year'].unique()[0], id='year-value'),
        html.Div([
            html.Div([
                html.Div([

                    "X value",
                    dcc.Dropdown(labels, list(labels.keys())[1], id='scatter-y-value',
                                 style={'width': '70%', 'height': '10%'}),
                ], style={'display': 'flex', 'flexDirection': 'column', 'height': '10%'}),

                html.Div([

                    "Y value",
                    dcc.Dropdown(labels, list(labels.keys())[0], id='scatter-x-value',
                                 style={'width': '70%', 'height': '10%'}),
                ], style={'display': 'flex', 'flexDirection': 'column', 'height': '10%'}),

                html.Div([

                    "size",
                    dcc.Dropdown(labels, list(labels.keys())[2], id='scatter-size-value',
                                 style={'width': '70%', 'height': '10%'}),
                ], style={'display': 'flex', 'flexDirection': 'column', 'height': '10%'}),

                dcc.Graph(id='scatter-graph', style={'width': '100%', 'height': '70%'})],
                style={'display': 'flex', 'flexDirection': 'column', 'width': '70%', 'height': '10%'}),
            dcc.Graph(id='pie-graph', style={'width': '30%', 'height': '10%'})],
            style={'display': 'flex', 'flexDirection': 'row'}),
        dcc.Graph(id='top-graph', style={'width': '100%', 'height': '10%'}),
    ],
        style={'display': 'flex', 'flexDirection': 'column'}),
], style={'display': 'flex', 'flexDirection': 'column'})


@callback(
    Output('line-graph', 'figure'),
    Input('country-val', 'value'),
    Input('line-y-value', 'value')
)
def line_graph(country, y_val):
    dff = df[df['country'].isin(country)].groupby('year', as_index=False)[y_val].sum()
    return px.line(x=dff['year'], y=dff[y_val], title=f'Annual {labels[y_val]}')


@callback(
    Output('scatter-graph', 'figure'),
    Input('year-value', 'value'),
    Input('scatter-x-value', 'value'),
    Input('scatter-y-value', 'value'),
    Input('scatter-size-value', 'value')
)
def scatter_graph(year_val, x_val, y_val, size_val):
    dff = df[df['year'] == year_val]
    return px.scatter(dff, x=x_val, y=y_val,
                      size=size_val, color="continent", hover_name="country",
                      log_x=True, title=f'The ratio of {labels[x_val]} to {labels[y_val]}')


@callback(
    Output('top-graph', 'figure'),
    Input('year-value', 'value'),
)
def top_graph(year_val):
    dff = df[df['year'] == year_val].sort_values('pop', ascending=False)[0:14]
    return px.bar(x=dff['country'], y=dff['pop'], title='Top 15 countries by population value')


@callback(
    Output('pie-graph', 'figure'),
    Input('year-value', 'value'),
)
def pie_graph(year_val):
    dff = df[df['year'] == year_val]
    return px.pie(names=dff['continent'], values=dff['pop'], title='Population on continents')


if __name__ == '__main__':
    app.run(debug=True)
