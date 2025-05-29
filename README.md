# 🏠 Njuškalo RSS Generator za Kuće

Automatski RSS generator za praćenje novih kuća na Njuškalo.hr

## 🚀 Postavljanje na GitHub Pages (PREPORUČENO)

### Korak 1: Stvori GitHub repozitorij
1. Idite na https://github.com i stvorite novi repozitorij
2. Nazovite ga npr. `njuskalo-kuce-rss`
3. Učinite ga javnim (Public)

### Korak 2: Upload kod
1. Uploadajte sve datoteke u repozitorij
2. **VAŽNO**: Promijenite u `vars.ini`:
   ```ini
   web_path = https://VASE-KORISNICKO-IME.github.io/njuskalo-kuce-rss/njuskalo-kuce.xml
   ```

### Korak 3: Omogući GitHub Pages
1. U vašem repozitoriju idite na **Settings**
2. Skrolajte do **Pages** (lijeva strana)
3. Pod **Source** odaberite **GitHub Actions**

### Korak 4: Pokreni prvi put
1. Idite na **Actions** tab
2. Kliknite na **"Generiraj Njuškalo RSS Feed"**
3. Kliknite **"Run workflow"** → **"Run workflow"**

### ✅ Gotovo!

RSS feed će biti dostupan na:
```
https://VASE-KORISNICKO-IME.github.io/njuskalo-kuce-rss/njuskalo-kuce.xml
```

## 📱 Dodavanje u RSS aplikaciju na mobitel

### Za Android:
1. **Feedly** (preporučujem):
   - Instalirajte iz Play Store
   - Dodajte feed s vašim GitHub Pages URL-om
   - Uključite push obavještenja

2. **Inoreader**:
   - Odličan za filtriranje po ključnim riječima
   - Ima keyword alerts

### Za iOS:
1. **NetNewsWire** (besplatan)
2. **Feedly**
3. **Reeder 5**

## ⚙️ Kako funkcionira

- GitHub Actions automatski pokreće skriptu **svakih 30 minuta**
- Provjerava nove oglase na Njuškalo.hr
- Generira ažurirani RSS feed
- Objavljuje na GitHub Pages

## 🛠️ Lokalno pokretanje (za testiranje)

```bash
pip install -r requirements.txt
python njuskalo-rssgen.py
```

## 📝 Prilagođavanje za druge kategorije

Promijenite u `vars.ini`:
```ini
[web]
page = https://www.njuskalo.hr/NOVA-KATEGORIJA

[rss]
title = Novi naslov
description = Novi opis
```

---

*RSS feed se automatski ažurira svakih 30 minuta. Nema potrebe za vlastitim serverom!*
