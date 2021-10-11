#!/usr/bin/env python

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd
import timeit
import pdb

starttime = timeit.default_timer()
# create the file to store result
csvfile = 'AdvChemIngredients.csv'
theaders = pd.DataFrame({'product page URL':[],
                         'product name':[] ,
                         'product code':[] ,
                         'ingredient':[] ,
                         'CAS#':[] ,
                         'function':[]})
theaders.to_csv(csvfile,header=True,index=False)

def page_soup(url):
    url = url
    # using this approach because the site sends 403 forbidden 
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    page_soup = soup(webpage, "lxml")
    return page_soup


def prod_urls(page_soup,class_):
    page_soup = page_soup
    prod_links = page_soup.find(class_=class_).find_all('a')
    prod_urls = []
    for prod in prod_links:
        prod_urls.append(prod.get('href'))
    return prod_urls


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
                except:
                    continue
            if len(row) > 0:
                row.insert(0, url)
                row.insert(1, prod_name)
                row.insert(2, prod_code)
                rows.append(row)
        df = pd.DataFrame(rows[0:], columns=rows[0])
        # df.to_csv('AdvChemIngredients.csv', mode = 'a', header=False, index=False)
    except AttributeError:
        rows = []
        row = []
        row.insert(0, url)
        row.insert(1, prod_name)
        row.insert(2, prod_code)
        rows.append(row)
        df = df.append(rows[0:])
    return df

main_url = 'https://www.advantagechemical.com/products/'
page = page_soup(main_url)
prod_type_url = prod_urls(page,"lander-children")

for url in prod_type_url:
    product_page = page_soup(url)
    product_url = prod_urls(product_page,"products-list")
    for url_name in product_url:
        df = table_extract(url_name)
        df.to_csv(csvfile, mode = 'a', header=False, index=False)

print(f"Scraping took - {timeit.default_timer() - starttime:.2f} seconds")









