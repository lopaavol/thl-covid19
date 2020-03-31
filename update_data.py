import os
import re
import requests
import pandas as pd

URL = 'https://thl.fi/fi/web/infektiotaudit-ja-rokotukset/ajankohtaista/ajankohtaista-koronaviruksesta-covid-19/tilannekatsaus-koronaviruksesta'
PATTERN = 'Päivitetty[\D]*(\d+)[\D]*\.[\D]*(\d+)'
HDFFILE = 'thl-data.h5'
COLS = ['Erityisvastuualue', 'Kokonaismäärä', 'Osastohoidossa', 'Tehohoidossa',
       'Kuolleet']

def parse_page(html):
    df = pd.read_html(html)[0]
    cols = df.loc[0,:].values
    df = pd.DataFrame(data=df.loc[1:,:].values, columns=cols)
    date = list(map(int,re.search(PATTERN, html).groups()))
    return date,df

def fetch_data(store):
    response = requests.get(URL)
    if response.status_code == 200:
        html = response.text
        date,df = parse_page(html)
        # Expect the information will be released only 2020
        datestr = "2020{:02d}{:02d}".format(date[1],date[0])
        key = "/thl_"+datestr
        if key not in store.keys():
            store[key] = df
            df.columns = COLS
            df['Date'] = datestr
            df = df.iloc[:-1,:]
            df.iloc[:,1:-1] = df.iloc[:,1:-1].astype('int32')
            if '/summary' in store.keys():
                summary = store['/summary']
                summary = pd.concat([summary,df], ignore_index=True)
            else:
                summary = df
            store['summary'] = summary
            return True
    return False

def main():
    store = pd.HDFStore(HDFFILE)
    status = fetch_data(store)
    store.close()

if __name__=="__main__":
    main()
