import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash()

# Layout
app.layout = html.Div(children=[
    html.Div(className="navbar", children=[
        html.A('MEDICAL SUPPLY STORE', style={'color' : 'red'}),
        html.A(''),
        html.A('Home'),
        html.A('Shop'),
        html.A('COVID-19', className="selected"),
        html.A('About')
    ]),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Div('Please select a comparison:', style={'font-family': 'arial', 'color': 'red', 'margin': '10px'}),
    dcc.Dropdown(
        id='select-comparison1',
        style={'font-family': 'arial'},
        options=[
            {'label': 'Total Cases - United States', 'value': 'us1'},
            {'label': 'Total Cases - World', 'value': 'world1'},
            {'label': 'Total Deaths - United States', 'value': 'us2'},
            {'label': 'Total Deaths - World', 'value': 'world2'},
        ],
        value='us1'
    ),
    dcc.Graph(id='graph1'),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': 'gray'}),
    html.Br(),
    html.Br(),
    html.Div('Please select a comparison:', style={'font-family': 'arial', 'color': 'red', 'margin': '10px'}),
    dcc.Dropdown(
        id='select-comparison2',
        style={'font-family': 'arial'},
        options=[
            {'label': 'Total Cases vs Total Deaths - United States', 'value': 'us1'},
            {'label': 'Total Cases vs Total Deaths - World', 'value': 'world1'},
            {'label': 'New Cases vs New Deaths - United States', 'value': 'us2'},
            {'label': 'New Cases vs New Deaths - World', 'value': 'world2'},
        ],
        value='us1'
    ),
    dcc.Graph(id='graph2'),

])


@app.callback(Output('graph1', 'figure'),
              [Input('select-comparison1', 'value')])
def update_figure1(selected_comparison):
    if selected_comparison == 'us1':
        df = pd.read_csv('../Datasets/time_series_covid19_confirmed_US.csv')
        df = df.groupby(['Province_State'])[df.columns[-1]].sum().reset_index()
        df = df.sort_values(by=[df.columns[-1]], ascending=[False]).head(10)
        data = [go.Bar(x=df['Province_State'], y=df[df.columns[-1]], marker={'color': 'red'})]
        return {'data': data,
                'layout': go.Layout(title='Total COVID-19 Cases in the Top 10 States', xaxis_title="State",
                                    yaxis_title="Total Number of Cases")}
    elif selected_comparison == 'world1':
        df = pd.read_csv('../Datasets/total_cases.csv')
        del df['date']
        del df['World']
        df = df.iloc[[-1]]
        df = pd.melt(df, value_name='total', var_name='country')
        df = df.sort_values(by=['total'], ascending=[False]).head(10)
        data = [go.Bar(x=df['country'], y=df['total'], marker={'color': 'red'})]
        return {'data': data,
                'layout': go.Layout(title='Total COVID-19 Cases in the Top 10 Countries', xaxis_title="Country",
                                    yaxis_title="Total Number of Cases")}
    elif selected_comparison == 'us2':
        df = pd.read_csv('../Datasets/time_series_covid19_deaths_US.csv')
        df = df.groupby(['Province_State'])[df.columns[-1]].sum().reset_index()
        df = df.sort_values(by=[df.columns[-1]], ascending=[False]).head(10)
        data = [go.Bar(x=df['Province_State'], y=df[df.columns[-1]], marker={'color': 'red'})]
        return {'data': data,
                'layout': go.Layout(title='Total COVID-19 Deaths in the Top 10 States', xaxis_title="State",
                                    yaxis_title="Total Number of Deaths")}
    elif selected_comparison == 'world2':
        df = pd.read_csv('../Datasets/total_deaths.csv')
        del df['date']
        del df['World']
        df = df.iloc[[-1]]
        df = pd.melt(df, value_name='total', var_name='country')
        df = df.sort_values(by=['total'], ascending=[False]).head(10)
        data = [go.Bar(x=df['country'], y=df['total'], marker={'color': 'red'})]
        return {'data': data,
                'layout': go.Layout(title='Total COVID-19 Deaths in the Top 10 Countries', xaxis_title="Country",
                                    yaxis_title="Total Number of Deaths")}


@app.callback(Output('graph2', 'figure'),
              [Input('select-comparison2', 'value')])
def update_figure2(selected_comparison):
    if selected_comparison == 'us1':
        df1 = pd.read_csv('../Datasets/total_cases.csv')
        df2 = pd.read_csv('../Datasets/total_deaths.csv')
        df1['date'] = pd.to_datetime(df1['date'])
        df2['date'] = pd.to_datetime(df2['date'])
        trace1 = go.Scatter(x=df1['date'], y=df1['United States'], mode='lines', name='Total Cases',
                            marker={'color': 'red'})
        trace2 = go.Scatter(x=df2['date'], y=df2['United States'], mode='lines', name='Total Deaths',
                            marker={'color': 'gray'})
        data = [trace1, trace2]
        return {'data': data, 'layout': go.Layout(title='Total COVID-19 Cases and Deaths in the US', xaxis_title="Date",
                                                  yaxis_title="Total Number")}
    elif selected_comparison == 'world1':
        df1 = pd.read_csv('../Datasets/total_cases.csv')
        df2 = pd.read_csv('../Datasets/total_deaths.csv')
        df1['date'] = pd.to_datetime(df1['date'])
        df2['date'] = pd.to_datetime(df2['date'])
        trace1 = go.Scatter(x=df1['date'], y=df1['World'], mode='lines', name='Total Cases',
                            marker={'color': 'red'})
        trace2 = go.Scatter(x=df2['date'], y=df2['World'], mode='lines', name='Total Deaths', marker={'color': 'gray'})
        data = [trace1, trace2]
        return {'data': data,
                'layout': go.Layout(title='Total COVID-19 Cases and Deaths in the World', xaxis_title="Date",
                                    yaxis_title="Total Number")}
    elif selected_comparison == 'us2':
        df1 = pd.read_csv('../Datasets/new_cases.csv')
        df2 = pd.read_csv('../Datasets/new_deaths.csv')
        df1['date'] = pd.to_datetime(df1['date'])
        df2['date'] = pd.to_datetime(df2['date'])
        trace1 = go.Scatter(x=df1['date'], y=df1['United States'], mode='lines', name='New Cases',
                            marker={'color': 'red'})
        trace2 = go.Scatter(x=df2['date'], y=df2['United States'], mode='lines', name=' New Deaths',
                            marker={'color': 'gray'})
        data = [trace1, trace2]
        return {'data': data, 'layout': go.Layout(title='New COVID-19 Cases and Deaths in the US', xaxis_title="Date",
                                                  yaxis_title="Total Number")}
    elif selected_comparison == 'world2':
        df1 = pd.read_csv('../Datasets/new_cases.csv')
        df2 = pd.read_csv('../Datasets/new_deaths.csv')
        df1['date'] = pd.to_datetime(df1['date'])
        df2['date'] = pd.to_datetime(df2['date'])
        trace1 = go.Scatter(x=df1['date'], y=df1['World'], mode='lines', name='New Cases',
                            marker={'color': 'red'})
        trace2 = go.Scatter(x=df2['date'], y=df2['World'], mode='lines', name='New Deaths', marker={'color': 'gray'})
        data = [trace1, trace2]
        return {'data': data,
                'layout': go.Layout(title='New COVID-19 Cases and Deaths in the World', xaxis_title="Date",
                                    yaxis_title="Total Number")}


if __name__ == '__main__':
    app.run_server()
