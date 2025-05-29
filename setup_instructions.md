# Postavljanje RSS obavještenja za Njuškalo kuće

## Korak 1: Instalacija
```bash
pip install -r requirements.txt
```

## Korak 2: Testiranje
```bash
python njuskalo-rssgen.py
```

## Korak 3: Automatsko pokretanje

### Windows Task Scheduler:
1. Otvorite Task Scheduler
2. Stvorite novu zadaću
3. Pokretanje: `run_rss.bat`
4. Interval: Svakih 30 minuta

### Linux/Mac cron:
```bash
# Dodajte u crontab
*/30 * * * * /path/to/your/python /path/to/njuskalo-rssgen.py
```

## Korak 4: Hostiranje RSS feed-a

### Opcija A: Lokalno s web serverom
```bash
python web_server.py
```
RSS će biti dostupan na: `http://localhost:5000/rss`

### Opcija B: Upload na web hosting
- Uploadajte `njuskalo-kuce.xml` na svoj web hosting
- Koristite FTP ili rsync za automatsko uploading

### Opcija C: GitHub Pages (besplatno)
1. Stvorite GitHub repozitorij
2. Postavite GitHub Actions za automatsko generiranje
3. RSS će biti dostupan na: `https://yourusername.github.io/repo/njuskalo-kuce.xml`

## Korak 5: Dodavanje u RSS aplikaciju

1. **Otvorite RSS aplikaciju** (Feedly, Inoreader, itd.)
2. **Dodajte novi feed** s URL-om vašeg RSS feed-a
3. **Postavite obavještenja** za novi sadržaj
4. **Konfigurirajte filtre** (po cijeni, lokaciji, itd.)

## Preporučene postavke obavještenja:

### Feedly:
- Ide na: "Settings" → "Notifications"
- Uključite: "New articles" za vaš feed
- Postavite: "Instant notifications"

### Inoreader:
- Ide na: "Preferences" → "Notifications"
- Dodajte "Keyword alert" za specifične pojmove
- Postavite push notifikacije

## Dodatni savjeti:

1. **Filtriraj po cijeni** - dodajte ključne riječi u `vars.ini`
2. **Provjeri feed redovito** - postavite kratki interval (15-30 min)
3. **Backup podataka** - redovito kopirajte `dump.pickle`

## Prilagođavanje za druge kategorije:

Za praćenje drugih kategorija, promijenite u `vars.ini`:
```ini
[web]
page = https://www.njuskalo.hr/nova-kategorija

[rss]
title = Novi naziv
description = Novi opis
file_name = novi-feed.xml
``` 