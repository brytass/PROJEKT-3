# Výsledky voleb – scraper

Tento projekt slouží k získávání výsledků voleb z webu [volby.cz](https://www.volby.cz) a ukládání dat do CSV souboru.

---

## 🚀 Instalace

1. Naklonujte nebo stáhněte tento repozitář.
2. Ujistěte se, že máte nainstalovaný **Python 3.9+**.
3. Nainstalujte potřebné knihovny:

```
pip install -r requirements.txt

Obsah requirements.txt:
requests
beautifulsoup4

Použití
Program se spouští z příkazové řádky se dvěma argumenty:
python main.py "<URL>" <vystupni_soubor.csv>
<URL> – odkaz na konkrétní okres z webu volby.cz
<vystupni_soubor.csv> – název výstupního CSV souboru

Příklad
Pokud chceme získat výsledky voleb v okrese Prostějov, použijeme:
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7106" vysledky_prostejov.csv

Ukázka výstupu (CSV)
Prvních pár sloupců výsledného souboru:

code,location,registered,envelopes,valid,Občanská demokratická strana,Česká str.sociálně demokrat.,...
589309,Atlachov,531,321,318,54,102,...
589317,Bedihošť,943,633,628,84,176,...
Výstup programu
Po dokončení běhu program vypíše:

Checking URL and file name
Fetching data from: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7106
Saved results to 'vysledky_prostejov.csv'.
CLOSING main.py
