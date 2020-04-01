import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as dhc
from dash.dependencies import Input, Output

HDFFILE = 'thl-data.h5'
WIDTH=1024

def create_layout(app, data):
    app.layout = dhc.Div(
        children=[
            dhc.Div(children=[
                dcc.Dropdown(
                    id='erityisvastuualue-dd',
                    options=[{'value': 'Koko maa', 'label': 'Koko maa'}]+[{'value': x, 'label': x} for i,x in enumerate(data['Erityisvastuualue'].drop_duplicates().values)],
                    multi=True,
                    value=['Koko maa'],
                )
            ]),
            dcc.Graph(id='graph')
        ],
        style={
            'width': WIDTH
        })


    @app.callback(
        Output('graph','figure'),
        [Input('erityisvastuualue-dd', 'value')])
    def update_graph(selection):
        dates = data['Date'].drop_duplicates().values
        x = ["{}-{}-{}".format(x[:4],x[4:6],x[6:]) for x in dates]
        cols = data.columns.values[1:-1]
        
        values = []
        for sel in selection:
            if sel == 'Koko maa':
                agg = data.groupby('Date').sum()
                for col in cols:
                    values.append({'x': x,
                                   'y': agg[col].values,
                                   'type': 'line',
                                   'name': sel.split(' ')[0]+': '+col})
            else:
                sdf = data[data[data.columns.values[0]]==sel]
                for col in cols:
                    values.append({'x': x,
                                   'y': sdf[col].values,
                                   'type': 'line',
                                   'name': sel.split(' ')[0]+': '+col})
    
        return {
            'data': values,
            'layout': {
                'title': 'THL data COVID-19',
                'width': WIDTH,
                'height': 600
            }
        }


    return app

def launch_site(data):
    app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
    app = create_layout(app, data)
    app.run_server(host='', debug=False)

def main():
    store = pd.HDFStore(HDFFILE)
    data = store['summary']
    store.close()
    launch_site(data)

if __name__=="__main__":
    main()
