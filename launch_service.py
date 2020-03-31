import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as dhc

HDFFILE = 'thl-data.h5'
COLS = ['Erityisvastuualue', 'Kokonaismäärä', 'Osastohoidossa', 'Tehohoidossa',
       'Kuolleet']

def launch_site(data):
    dates = data['Date'].drop_duplicates().values
    x = ["{}-{}-{}".format(x[:4],x[4:6],x[6:]) for x in dates]
    agg = data.groupby('Date').sum()
    cols = agg.columns.values[1:]
    values = []
    for col in cols:
        values.append({'x': x, 'y': agg[col].values, 'type': 'line', 'name': col})
    app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
    app.layout = dhc.Div(children=[
        dcc.Graph(
            id='graph',
            figure={
                'data': values,
                'layout': {
                    'title': 'THL data COVID-19'
                }
            }
        )
    ])
    app.run_server()

def main():
    store = pd.HDFStore(HDFFILE)
    data = store['summary']
    store.close()
    launch_site(data)

if __name__=="__main__":
    main()
