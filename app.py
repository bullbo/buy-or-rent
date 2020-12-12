# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objects as go


def _intrest(arr, rate):
  for i in range(1,len(arr)):
    arr[i] = arr[i-1]*rate
  return arr


def calcs(years, rent, rent_increase, loan, intrest, amort, fee, fee_increase):
    ones = np.ones(years)
    years = np.arange(1, years+1)
    rent = rent*12
    fee = fee*12
    rent_increase /= 100
    amort /= 100
    intrest /= 100
    fee_increase /= 100

    amort_left = _intrest(loan*ones, 1-amort)

    yearly_rent = _intrest(rent*ones, 1+rent_increase)
    yearly_fee = _intrest(fee*ones, 1+fee_increase)
    yearly_intrest = amort_left*intrest
    yearly_buy = yearly_fee+yearly_intrest

    cost_rent = np.cumsum(yearly_rent)
    cost_fee = np.cumsum(yearly_fee)
    cost_intrest = np.cumsum(yearly_intrest)
    cost_buy = np.cumsum(yearly_buy)

    return {"yearly-rent"   : yearly_rent,
            "yearly-fee"    : yearly_fee,
            "yearly-intrest": yearly_intrest,
            "yearly-buy"    : yearly_buy,
            "cost-rent"     : cost_rent, 
            "cost-fee"      : cost_fee,
            "cost-intrest"  : cost_intrest,
            "cost-buy"      :cost_buy,
            "amort-left"    : amort_left}


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title= "BoR"

app.layout = html.Div(children=[
    html.H1(children='BoR: Buy or Rent'),

    html.Div(children='''
        A web application that simplifies and visualises the costs that arises from buying versus renting a house.
    '''),

    html.H2("Parameters:"),
    dcc.RadioItems(
        id='toggle',
        options=[{'label': i, 'value': i} for i in ['Show', 'Hide']],
        value='Show'
    ),
    html.Div(id='params', children=[
        html.Div(id='updatemode-output-container', style={'margin-top': 20}),
        html.H6("Total Years:"),
        dcc.Slider(
        id = 'tot-years',
        min=1,
        max=100,
        value=50,
        tooltip = { 'always_visible': False },
        marks={'0': '0', '50': '50', '100': '100'},
        included=False),

        html.H6("Rent:"),
        dcc.Slider(
        id = 'rent',
        min=1000,
        max=20000,
        value=6500,
        tooltip = { 'always_visible': False },
        marks={'1000': '1000', '20000': '20000'},
        included=False),

        html.H6("Rent Yearly Increase (%):"),
        dcc.Slider(
        id = 'rent-increase',
        min=0.0,
        max=5.0,
        value=1.0,
        step=0.1,
        tooltip = { 'always_visible': False },
        marks={'0': '0%', '5': '5%'},
        included=False),

        html.H6("Total Loan:"),
        dcc.Slider(
        id = 'loan',
        min=500000,
        max=10000000,
        value=4000000,
        tooltip = { 'always_visible': False },
        marks={'500000': '500,000', '10000000': '10,000,000'},
        included=False),

        html.H6("Yearly Intrest (%):"),
        dcc.Slider(
        id = 'intrest',
        min=0.0,
        max=5.0,
        value=3.0,
        step=0.1,
        tooltip = { 'always_visible': False },
        marks={'0': '0%', '5': '5%'},
        included=False),

        html.H6("Yearly Amortization (%):"),
        dcc.Slider(
        id = 'amort',
        min=0.0,
        max=10.0,
        value=2.0,
        step=0.1,
        tooltip = { 'always_visible': False },
        marks={'0': '0%', '10': '10%'},
        included=False),


        html.H6("Monthly Fee:"),
        dcc.Slider(
        id = 'fee',
        min=500,
        max=20000,
        value=4000,
        tooltip = { 'always_visible': False },
        marks={'500': '500', '20000':'20000'},
        included=False),

        html.H6("Yearly Fee Increase (%):"),
        dcc.Slider(
        id = 'fee-increase',
        min=0.0,
        max=5.0,
        value=1.0,
        step=0.1,
        tooltip = { 'always_visible': False },
        marks={'0': '0%', '5': '5%'},
        included=False)
        ]),

    

    html.H3("Yearly Costs:"),
    dcc.Graph(id='yearly-costs'),
    html.H3("Accumulated Costs:"),
    dcc.Graph(id='accumulated-costs'),
   
])

@app.callback(Output('yearly-costs', 'figure'), 
              Output('accumulated-costs', 'figure'),
              Input('tot-years', 'value'),
              Input('rent','value'),
              Input('rent-increase', 'value'),
              Input('loan', 'value'),
              Input('intrest', 'value'),
              Input('amort', 'value'),
              Input('fee', 'value'),
              Input('fee-increase', 'value'),)
def update_figure(tot_years, rent, rent_increase, loan, intrest, amort, fee, fee_increase):
    results = calcs(tot_years, rent, rent_increase, loan, intrest, amort, fee, fee_increase)

    fig_yearly = go.Figure()
    fig_acc = go.Figure()

    fig_yearly.add_trace(go.Scatter(y=results['yearly-rent'], name="Total Rent Cost", line=dict(width= 4)))
    fig_yearly.add_trace(go.Scatter(y=results['yearly-fee'], name="Fee Cost", line=dict(dash='dash')))
    fig_yearly.add_trace(go.Scatter(y=results['yearly-intrest'], name="Intrest Cost", line=dict(dash='dash')))
    #fig_yearly.add_trace(go.Scatter(y=results['amort-left'], name="Amortization Left", line=dict(dash='dash')))
    fig_yearly.add_trace(go.Scatter(y=results['yearly-buy'], name="Total Buy Cost (Fee + Intrest)", line=dict(width= 4)))
    
    fig_acc.add_trace(go.Scatter(y=results['cost-rent'], name="Money Spent on Rent", line=dict(width= 4)))
    fig_acc.add_trace(go.Scatter(y=results['cost-fee'], name="Money Spent on Fee", line=dict(dash='dash')))
    fig_acc.add_trace(go.Scatter(y=results['cost-intrest'], name="Money Spent Intrest", line=dict(dash='dash')))
    fig_acc.add_trace(go.Scatter(y=results['cost-buy'], name="Money Spent to Buy (Fee + Intrest)", line=dict(width= 4)))


    fig_yearly.update_layout(xaxis_title="Years", yaxis_title="Cost")
    fig_acc.update_layout(xaxis_title="Years", yaxis_title="Cost")

    return fig_yearly, fig_acc

@app.callback(Output('params', 'style'), [Input('toggle', 'value')])
def toggle_container(toggle_value):
    if toggle_value == 'Show':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

if __name__ == '__main__':
    app.run_server(debug=True)