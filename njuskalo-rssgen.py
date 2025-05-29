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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(conf.get('web', 'page'), timeout=30, headers=headers)
    response.raise_for_status()
    print(f"HTTP status: {response.status_code}")
    
    # Debug - spremi HTML za analizu
    with open('debug_page.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(f"HTML stranica spremljena kao debug_page.html ({len(response.text)} chars)")
    
    doc = html5lib.parse(response.content, treebuilder='lxml')
except Exception as e:
    print(f"Greška pri dohvaćanju stranice: {e}")
    # Stvorit ćemo prazan RSS feed ako stranica ne radi
    L = []
    doc = None

L = []
article_count = 0

if doc is not None:
    print("Analiziram HTML strukturu...")
    
    # Debug - pronađi sve article elemente
    articles = []
    for element in doc.iter():
        if element.tag == '{http://www.w3.org/1999/xhtml}article':
            articles.append(element)
            article_count += 1
            
    print(f"Pronađeno {len(articles)} article elemenata")
    
    # Debug - pronađi sve elemente s različitim klasama
    entity_titles = []
    entity_descriptions = []
    entity_prices = []
    
    for element in doc.iter():
        if hasattr(element, 'attrib') and element.attrib.get('class'):
            class_name = element.attrib.get('class', '')
            if 'entity-title' in class_name:
                entity_titles.append(element)
            elif 'entity-description' in class_name:
                entity_descriptions.append(element)
            elif 'entity-price' in class_name or 'price' in class_name.lower():
                entity_prices.append(element)
    
    print(f"Debug: entity-title elemenata: {len(entity_titles)}")
    print(f"Debug: entity-description elemenata: {len(entity_descriptions)}")
    print(f"Debug: price elemenata: {len(entity_prices)}")
    
    # Pokušajmo s različitim pristupom - tražimo linkove koji vode na /oglas/
    links = []
    for element in doc.iter():
        if element.tag == '{http://www.w3.org/1999/xhtml}a':
            href = element.attrib.get('href', '')
            if '/oglas/' in href:
                links.append({
                    'href': href,
                    'text': element.text or '',
                    'class': element.attrib.get('class', '')
                })
    
    print(f"Debug: Pronađeno {len(links)} linkova s /oglas/")
    
    if links:
        print("Primjer linkova:")
        for i, link in enumerate(links[:5]):
            print(f"  {i+1}. href={link['href']}, text='{link['text']}', class='{link['class']}'")
    
    # Ako nema standardnih article elemenata, pokušajmo s linkovma
    if not articles and links:
        print("Koristim linkove umjesto article elemenata...")
        for i, link in enumerate(links[:20]):  # Uzmi prvih 20 linkova
            D = {
                'name': f"oglas_{i}_{int(time.time())}",
                'href': f"http://www.njuskalo.hr{link['href']}" if link['href'].startswith('/') else link['href'],
                'title': link['text'].encode('utf-8') if link['text'] else b'Bez naslova',
                'text': b'Opis nije dostupan',
                'price': b'Cijena na upit',
                'time': time.time(),
                'datetime': datetime.datetime.now()
            }
            L.append(D)
    else:
        # Originalni kod za article elemente
        for element in doc.iter():
            if element.tag == '{http://www.w3.org/1999/xhtml}article':
                D = {}
                for i in list(element):
                    if i.attrib.get('class') == 'entity-title':
                        tmp = i.getchildren()
                        if tmp:
                            D['name'] = tmp[0].attrib.get('name', '')
                            D['href'] = "http://www.njuskalo.hr/" + tmp[0].attrib.get('href', '')
                            D['title'] = tmp[0].text.encode('utf-8') if tmp[0].text else b'Nema naslova'
                            D['time'] = time.time()
                            D['datetime'] = datetime.datetime.now()
                            
                    if i.attrib.get('class') == 'entity-description':
                        tmp = i.getchildren()
                        if tmp and tmp[0].text:
                            D['text'] = tmp[0].text.encode('utf-8').strip()
                        else:
                            D['text'] = b'Nema opisa'
                            
                    if i.attrib.get('class') == 'entity-prices':
                        tmp = i.getchildren()
                        if tmp and tmp[0].getchildren():
                            price_elem = tmp[0].getchildren()[0].getchildren()
                            if price_elem:
                                D['price'] = price_elem[0].text.encode('utf-8').strip() if price_elem[0].text else b'Cijena na upit'
                            else:
                                D['price'] = b'Cijena na upit'
                        else:
                            D['price'] = b'Cijena na upit'
                            
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

# Generiraj RSS feed čak i ako nema oglasa
def create_rss_item(x):
    return PyRSS2Gen.RSSItem(
        title=f"{x['title'].decode('utf-8')} [{x['price'].decode('utf-8')}]",
        link=x['href'],
        description=x['text'].decode('utf-8'),
        guid=x['name'],
        pubDate=x.get('datetime')
    )

# Ako nema oglasa, stvorit ćemo placeholder
if not L2:
    print("Nema oglasa, stvaram placeholder RSS")
    L2 = [{
        'title': b'Nema novih oglasa',
        'price': b'N/A',
        'href': 'https://www.njuskalo.hr/prodaja-kuca/krapinsko-zagorska',
        'text': b'RSS feed je aktivan, čeka se pojavljivanje novih oglasa.',
        'name': 'placeholder',
        'datetime': datetime.datetime.now()
    }]

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

# Debug - ispiši početak RSS datoteke
try:
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()[:500]
        print("Početak RSS datoteke:")
        print(content)
except Exception as e:
    print(f"Greška pri čitanju RSS datoteke: {e}") 