#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import html5lib
import PyRSS2Gen
import datetime
import lxml
import requests
import pickle
import time
import os
from configparser import ConfigParser

# Učitaj konfiguraciju
conf = ConfigParser()
conf.read("./vars.ini")

print(f"Dohvaćam stranicu: {conf.get('web', 'page')}")

try:
    # Koristimo requests umjesto urllib
    response = requests.get(conf.get('web', 'page'), timeout=30)
    response.raise_for_status()
    doc = html5lib.parse(response.content, treebuilder='lxml')
except Exception as e:
    print(f"Greška pri dohvaćanju stranice: {e}")
    exit(1)

L = []

# Parsiranje oglasa
for element in doc.iter():
    if element.tag == '{http://www.w3.org/1999/xhtml}article':
        D = {}
        for i in list(element):
            if i.attrib.get('class') == 'entity-title':
                tmp = i.getchildren()
                if tmp:
                    D['name'] = tmp[0].attrib.get('name', '')
                    D['href'] = "http://www.njuskalo.hr/" + tmp[0].attrib.get('href', '')
                    D['title'] = tmp[0].text.encode('utf-8') if tmp[0].text else 'Nema naslova'
                    D['time'] = time.time()
                    D['datetime'] = datetime.datetime.now()
                    
            if i.attrib.get('class') == 'entity-description':
                tmp = i.getchildren()
                if tmp and tmp[0].text:
                    D['text'] = tmp[0].text.encode('utf-8').strip()
                else:
                    D['text'] = 'Nema opisa'
                    
            if i.attrib.get('class') == 'entity-prices':
                tmp = i.getchildren()
                if tmp and tmp[0].getchildren():
                    price_elem = tmp[0].getchildren()[0].getchildren()
                    if price_elem:
                        D['price'] = price_elem[0].text.encode('utf-8').strip() if price_elem[0].text else 'Cijena na upit'
                    else:
                        D['price'] = 'Cijena na upit'
                else:
                    D['price'] = 'Cijena na upit'
                    
                # Dodaj oglas u listu samo ako imamo osnovne podatke
                if 'name' in D and 'title' in D:
                    L.append(D)

print(f"Pronađeno {len(L)} oglasa")

# Učitaj postojeće oglase iz pickle datoteke
try:
    with open('dump.pickle', 'rb') as fdump:
        tmp = pickle.load(fdump)
        L2 = tmp['data']
        L2names = [x['name'] for x in L2]
        
        # Dodaj nove oglase
        novi_oglasi = 0
        for x in L:
            if x['name'] not in L2names:
                L2names.append(x['name'])
                L2.append(x)
                novi_oglasi += 1
                
        print(f"Dodano {novi_oglasi} novih oglasa")
        
        # Ukloni stare oglase (starije od 2 dana)
        L2 = [x for x in L2 if x.get('time') is not None
              and (time.time() - x['time']) < 172800]
              
except (IOError, FileNotFoundError):
    print("Stvaram novu pickle datoteku")
    L2 = L

# Spremi ažurirane podatke
with open('dump.pickle', 'wb') as fdump:
    pickle.dump({'data': L2}, fdump)

# Generiraj RSS feed
def create_rss_item(x):
    return PyRSS2Gen.RSSItem(
        title=f"{x['title'].decode('utf-8')} [{x['price'].decode('utf-8')}]",
        link=x['href'],
        description=x['text'].decode('utf-8'),
        guid=x['name'],
        pubDate=x.get('datetime')
    )

rssitems = [create_rss_item(x) for x in L2]

rss = PyRSS2Gen.RSS2(
    title=conf.get('rss', 'title'),
    link=conf.get('rss', 'web_path'),
    description=conf.get('rss', 'description'),
    lastBuildDate=datetime.datetime.now(),
    items=rssitems
)

# Spremi RSS datoteku
output_path = conf.get('rss', 'file_path') + conf.get('rss', 'file_name')
with open(output_path, 'w', encoding='utf-8') as f:
    rss.write_xml(f)

print(f"RSS feed generiran: {output_path}")
print(f"Ukupno oglasa u feedu: {len(rssitems)}") 