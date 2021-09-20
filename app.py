import mysql.connector 
import pandas as pd
import numpy as np
import dash
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import plotly.graph_objs as go
import plotly.express as px

app = dash.Dash(__name__)
df = pd.read_csv('data/dash_data.csv' , parse_dates=['date'])


territory = set(df['TerritoryName'])
df['Year'] = df['date'].dt.year
year = set(df['Year'])

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.H3("VP Dashboard", style={"margin-bottom": "0px", 'color': 'white', 'textAlign': 'center'}),
                html.H5("Data Analytics on Posted Leads(2017-2021)", style={"margin-top": "0px", 'color': 'white' , 'textAlign': 'center'}),
            ])
        ])
    ]),
    
    
    html.Div([
        html.Div([
            html.H6(children='Overall Leads Posted',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(f"{df.id.count()}",
                   style={
                       'textAlign': 'center',
                       'color': 'orange',
                       'fontSize': 40},
                 )], className="card_container four columns",
        ),
        html.Div([
            html.H6(children='Overall Active Leads',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(df[df['LeadStatusName']=="Active"].id.count(),
                   style={
                       'textAlign': 'center',
                       'color': 'green',
                       'fontSize': 40},
                 )], className="card_container four columns",
        ),
        html.Div([
            html.H6(children='Overall De-active Leads',
                    style={
                        'textAlign': 'center',
                        'color': 'white'}
                    ),

            html.P(df[df['LeadStatusName'] == "De-active"].id.count(),
                   style={
                       'textAlign': 'center',
                       'color': 'red',
                       'fontSize': 40},
                 )], className="card_container four columns",
        ),
    ], className="row flex-display"),
    
    html.Div([
        html.Div([
            html.P('Select Country:', className='fix_label',  style={'color': 'white'}),
            dcc.Dropdown(id='memory-countries', 
                         multi=False,
                         clearable=True,
                         value='Asia',
                         options=[{'value': x, 'label': x} for x in territory],  
                         className='dcc_compon'),
            html.P('Select Year:', className='fix_label',  style={'color': 'white'}),
            dcc.Dropdown(
                id='memory-year', 
                multi=False,
                clearable=True,
                value = 2017,
                options=[{'value': x, 'label': x} for x in year], 
                className='dcc_compon', 
            ),
            dcc.Graph(id='posted_leads', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},
                     ),
            dcc.Graph(id='active', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},
                     ),
            dcc.Graph(id='de-active', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},
                     ),
        ], className="create_container three columns", id="cross-filter-options"),
        html.Div([
            dcc.Graph(id='technologies-pie-graph',
                      config={'displayModeBar': 'hover'}),
        ], className="create_container four columns"),
        html.Div([
            dcc.Graph(id="top-5-technologies")
        ], className="create_container five columns"),
    ], className="row flex-display"
    ),
    
    html.Div([       
        html.Div([
            dcc.Graph(id='horizontal-bar-graph'),
        ], className="create_container eight columns"),
        html.Div([
            dcc.Graph(id='pie-graph',
                      config={'displayModeBar': 'hover'}),
        ], className="create_container four columns"),      
    ], className="row flex-display"),
    
    html.Div([
        html.Div([
           dcc.Graph(id='memory-graph',config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},)
        ], className="create_container six columns"),
        
        html.Div([
            dcc.Graph(id='line-graph',config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},),
        ], className="create_container six columns"),
    ], className="row flex-display"),
    
    
    html.Div([
        html.Div([
           dcc.Graph(id='size-bar-graph',config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},)
        ], className="create_container twelve columns"),
    ], className="row flex-display"),
    
    html.Div([
        html.Div([
           dcc.Graph(id='domain_graph',config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'},)
        ], className="create_container twelve columns"),
    ], className="row flex-display"),
    
])

@app.callback(Output('posted_leads', 'figure'),
              [Input('memory-countries', 'value'),
             Input('memory-year', 'value')])
def update_posted_leads(day , year_value):
    line_data = df[(df['TerritoryName'] == day) & (df['Year'] == year_value)]
    posted_leads_value = line_data.id.count()
    return {
            'data': [
                go.Indicator(
                    value=posted_leads_value,
                    number={'valueformat': ',',
                            'font': {'size': 20},
                           },
                    domain={'y': [0, 1], 'x': [0, 1]}
                )],
            'layout': go.Layout(
                title={'text': 'Posted Leads',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top',
                      },
                font=dict(color='orange'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50,
                ),

            }

@app.callback(Output('active', 'figure'),
              [Input('memory-countries', 'value'),
             Input('memory-year', 'value')])
def update_active_leads(day , year_value):
    line_data = df[(df['TerritoryName'] == day) & (df['Year'] == year_value) & 
                   (df['LeadStatusName']== "Active")]
    active_leads_value = line_data.id.count()
    return {
            'data': [
                go.Indicator(
                    value=active_leads_value,
                    number={'valueformat': ',',
                            'font': {'size': 20},
                           },
                    domain={'y': [0, 1], 'x': [0, 1]}
                )],
            'layout': go.Layout(
                title={'text': 'Active Leads',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top',
                      },
                font=dict(color='green'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50,
                ),

            }

@app.callback(Output('de-active', 'figure'),
              [Input('memory-countries', 'value'),
             Input('memory-year', 'value')])
def update_deactive_leads(day , year_value):
    line_data = df[(df['TerritoryName'] == day) & (df['Year'] == year_value) & 
                   (df['LeadStatusName']== "De-active")]
    deactive_leads_value = line_data.id.count()
    return {
            'data': [
                go.Indicator(
                    value=deactive_leads_value,
                    number={'valueformat': ',',
                            'font': {'size': 20},
                           },
                    domain={'y': [0, 1], 'x': [0, 1]}
                )],
            'layout': go.Layout(
                title={'text': 'De-Active Leads',
                       'y': 1,
                       'x': 0.5,
                       'xanchor': 'center',
                       'yanchor': 'top',
                      },
                font=dict(color='red'),
                paper_bgcolor='#1f2c56',
                plot_bgcolor='#1f2c56',
                height=50,
                ),

            }




@app.callback(Output('top-5-technologies', 'figure'),
              [Input('memory-countries', 'value'),
             Input('memory-year', 'value')])
    
def update_top_technologies(day , year_value):
    line_data = df[(df['TerritoryName'] == day) & (df['Year'] == year_value)]
    line_data['TechnologyName'].count()
    filter_data = line_data.groupby(['TechnologyName']).agg({'id':'count'})
    line_data= pd.DataFrame(filter_data.reset_index())
    line_data = line_data.nlargest(5, ['id'])
    fig = px.bar(line_data, x="TechnologyName", y="id",text='id',
                 title="Top 5 Technologies" ,labels={'TechnologyName': 'Technology', 'id':'Lead Count'})
    fig.update_layout(plot_bgcolor='#1f2c56',
                  paper_bgcolor='#1f2c56',  titlefont={'color': 'white','size': 20},
                  font_color='white',
                  autosize=True,
                      title_x=0.5
                 )
    fig.update_xaxes(gridwidth =0, gridcolor ="grey" , showline= True , showgrid=False)
    fig.update_yaxes(gridwidth =0 , gridcolor ="grey" , showline = True )
    return fig

@app.callback(Output('memory-graph', 'figure'),
              [Input('memory-countries', 'value'),
             Input('memory-year', 'value')])

def update_bar_chart(day , year_value): 
    line_data = df[(df['TerritoryName'] == day) & (df['Year'] == year_value)]
    line_data['Mon_Year'] = line_data['date'].dt.strftime('%b %Y')
    filter_data = line_data.groupby(['Mon_Year','LeadStatusName']).agg({'id':'count'})
    line_data= pd.DataFrame(filter_data.reset_index())
    fig = px.line(line_data , x = "Mon_Year" , y ="id" , color="LeadStatusName",title='Variation Of Leads Month Wise',labels={'id':'Lead Count'})
    fig.update_layout(plot_bgcolor='#1f2c56',
                  paper_bgcolor='#1f2c56',  titlefont={'color': 'white','size': 20},
                  font_color='white',
                  autosize=True,
                      title_x=0.5
                 )
    fig.update_xaxes(gridwidth =0, gridcolor ="grey" , showline= True , showgrid=False)
    fig.update_yaxes(gridwidth =0 , gridcolor ="grey" , showline = True )
    return fig

@app.callback(Output('line-graph', 'figure'),
              [Input('memory-countries', 'value'),
               Input('memory-year', 'value')])

def update_line_chart(day ,year_value ): 
    line_data = df[(df['TerritoryName'] == day) & (df['Year'] == year_value)]
    line_data['Mon_Year'] = line_data['date'].dt.strftime('%b %Y')
    filter_data = line_data.groupby(['Mon_Year']).agg({'id':'count'})
    line_data= pd.DataFrame(filter_data.reset_index())
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=line_data['Mon_Year'], y=line_data['id'],
                    mode='lines+markers'))
    fig.update_layout(plot_bgcolor='#1f2c56',
                      paper_bgcolor='#1f2c56',  titlefont={'color': 'white','size': 20},
                      font_color='white',
                      autosize=True,
                      title_x=0.5,
                      title='Total Leads Per Month',
                      xaxis_title='Mon_Year',
                      yaxis_title='Lead Count')
    fig.update_xaxes(gridwidth =0, gridcolor ="grey" , showline= True , showgrid=False)
    fig.update_yaxes(gridwidth =0 , gridcolor ="grey" , showline = True )
    return fig



@app.callback(Output('pie-graph', 'figure'),
              [Input('memory-countries', 'value'),
              Input('memory-year', 'value')]
             )
def update_pie_chart(day ,year_value):
    line_data = df[(df['TerritoryName'] == day) & (df['Year'] == year_value)]
    filter_data = line_data.groupby(['LeadStatusName']).agg({'id':'count'})
    line_data= pd.DataFrame(filter_data.reset_index())
    posted_leads_count = line_data.id.sum()
    line_data.loc[len(line_data.index)] = ['Posted Leads',posted_leads_count]
    return {
        'data': [
            go.Pie(labels=line_data['LeadStatusName'].tolist(),
            values=line_data['id'].tolist(),
            hoverinfo='label+value+percent',
            textinfo='label+value',
            textfont=dict(size=13),
            hole=.7,
            rotation=45
                  )],
        'layout': go.Layout(
            plot_bgcolor='#1f2c56',
            paper_bgcolor='#1f2c56',
            hovermode='closest',
            title={
                'text': 'Lead Status Distribution: ',
                'y': 0.93,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
            titlefont={
                       'color': 'white',
                       'size': 20},
            legend={
                'orientation': 'h',
                'bgcolor': '#1f2c56',
                'xanchor': 'center', 'x': 0.5, 'y': -0.07},
            font=dict(
                family="sans-serif",
                size=12,
                color='white')
        ),
    }

@app.callback(Output('technologies-pie-graph', 'figure'),
              [Input('memory-countries', 'value'),
             Input('memory-year', 'value')])
def update_technologies_pie_graph(day , year_value): 
    filter_data = df.groupby(['TerritoryName','TechnologyName','Year']).agg({'id':'count'})
    line_data= pd.DataFrame(filter_data.reset_index())
    line_data = line_data[(line_data['TerritoryName'] == day) & (line_data['Year'] == year_value)] 
    fig = px.pie(line_data, values='id', names='TechnologyName', title='Technology Requirement Distribution',labels={'id':'Lead Count'})
    fig.update_layout(plot_bgcolor='#1f2c56',
                  paper_bgcolor='#1f2c56',  titlefont={'color': 'white','size': 20},
                  font_color='white',
                  autosize=True,
                       title_x=0.5
                 )
    return fig
    

@app.callback(Output('horizontal-bar-graph', 'figure'),
              [Input('memory-countries', 'value'),
             Input('memory-year', 'value')])
def update_horizontal_graph(day , year_value): 
    filter_data = df.groupby(['TerritoryName','TechnologyName','LeadStatusName','Year']).agg({'id':'count'})
    line_data= pd.DataFrame(filter_data.reset_index())
    line_data = line_data[(line_data['TerritoryName'] == day) & (line_data['Year'] == year_value)]
    fig = px.bar(line_data, x="id", y="TechnologyName", color='LeadStatusName', orientation='h',
                  height=400,
                  text = "id",
                  title='Lead Status Distribution By Technology' , 
                 labels={'id':'Lead Count' , 'TechnologyName' : 'Technology'})
    fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    fig.update_layout(plot_bgcolor='#1f2c56',
                  paper_bgcolor='#1f2c56',  titlefont={'color': 'white','size': 20},
                  font_color='white',
                  autosize=True,
                       title_x=0.5
                       
                 )
    fig.update_xaxes(gridwidth =0, gridcolor ="grey" , showline= True , showgrid=False)
    fig.update_yaxes(gridwidth =0 , gridcolor ="grey" , showline = True )
    return fig

@app.callback(Output('size-bar-graph', 'figure'),
              [Input('memory-countries', 'value'),
             Input('memory-year', 'value')])
def update_size_bar_graph(day , year_value): 
    filter_data = df.groupby(['TerritoryName','DomainName','Year']).agg({'hours':'mean'})
    line_data= pd.DataFrame(filter_data.reset_index())
    line_data = line_data[(line_data['TerritoryName'] == day) & (line_data['Year'] == year_value)]
    fig = px.bar(line_data, x="DomainName", y="hours",text = "hours",title="Average Time Required For Project",labels={'hours':'Average_hours'})
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(plot_bgcolor='#1f2c56',
                  paper_bgcolor='#1f2c56',  titlefont={'color': 'white','size': 20},
                  font_color='white',
                  autosize=True,
                title_x=0.5
                 )
    fig.update_xaxes(gridwidth =0, gridcolor ="grey" , showline= True , showgrid=False)
    fig.update_yaxes(gridwidth =0 , gridcolor ="grey" , showline = True )
    return fig


@app.callback(Output('domain_graph', 'figure'),
              [Input('memory-countries', 'value'),
             Input('memory-year', 'value')])
def update_size_bar_graph(day , year_value): 
    line_data = df[(df['TerritoryName'] == day) & (df['Year'] == year_value)]
    filter_data = line_data.groupby(['DomainName','TechnologyName']).agg({'id':'count'})
    line_data= pd.DataFrame(filter_data.reset_index())
    fig = px.bar(line_data, x="id", y="TechnologyName", color='DomainName',barmode='stack',
                  height=400,
                  text = "id",
                  title='Domains Distribution For Each Technology' , 
                 labels={'id':'Count' , 'TechnologyName' : 'Technology'})
    fig.update_layout(plot_bgcolor='#1f2c56',
                  paper_bgcolor='#1f2c56',  titlefont={'color': 'white','size': 20},
                  font_color='white',
                  autosize=True,
                title_x=0.5
                 )
    fig.update_xaxes(gridwidth =0, gridcolor ="grey" , showline= True , showgrid=False)
    fig.update_yaxes(gridwidth =0 , gridcolor ="grey" , showline = True )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, threaded=True, port=10450)