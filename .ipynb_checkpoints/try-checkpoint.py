from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import pdb

# create the file to store result
csvfile = 'try.csv'
theaders = pd.DataFrame({'product page URL':[], 'product name':[] , 'product code':[] ,'ingredient':[] ,'CAS#':[] ,'function':[]})
theaders.to_csv(csvfile,header=True,index=False)

def table_extract(url):
    url = url
    prod_name = url.split('/')[-1]
    prod_code = ''
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup = soup(webpage, "lxml")
    df = pd.DataFrame()
    try:
        table = page_soup.find(class_="product-details product-details--full-width product-details--ingredients").find('table')
        rows = []
        for child in table.tbody.children:
            row = []
            for td in child:
                try:
                    row.append(td.text.replace('\n', ''))
                    # pdb.set_trace()
                except:
                    continue
            if len(row) > 0:
                row.insert(0, url)
                row.insert(1, prod_name)
                row.insert(2, prod_code)
                rows.append(row)
        # pdb.set_trace()
        df = pd.DataFrame(rows[0:], columns=rows[0])
        df.to_csv(csvfile, mode = 'a', header=False, index=False)
    except AttributeError:
        rows = pd.DataFrame(url,prod_name,prod_code,'','','')
        df = df.append(rows)
        df.to_csv(csvfile, mode = 'a', header=False, index=False)



urls = ['https://www.advantagechemical.com/products/three-compartment-sink/sani-tablets',
        'https://www.advantagechemical.com/products/three-compartment-sink/sani-quat']

for url in urls:
    table_extract(url)
