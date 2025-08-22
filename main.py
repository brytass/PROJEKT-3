"""
main.py: třetí projekt do Engeto Online Python Akademie
author: Radek Marval
email: marvalradek@seznam.cz
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys

BASE = "https://www.volby.cz/pls/ps2017nss/"

def fetch_html(url):
    """stáhne HTML stránku z URL a převede ji na BeautifulSoup objekt."""
    return BeautifulSoup(requests.get(url).text, "html.parser")

def collect_municipality_urls(main_url):
    """z hlavní stránky okresu získá seznam kódů a URL jednotlivých obcí."""
    soup = fetch_html(main_url)
    urls = []
    for tag in soup.select("td.cislo a"):
        full_url = BASE + tag["href"]  #doplní základní URL
        code = tag.text.strip()        #kód obce
        urls.append((code, full_url))
    return urls

def parse_general_info(soup):
    """získá základní informace o obci: název, registrovaní, odevzdané obálky a platné hlasy."""
    data = {}
    # lambda t: t and "Obec:" in t
    # t je text každého <h3> prvku
    # vrátí True, pokud text obsahuje "Obec:"
    h3 = soup.find("h3", string=lambda t: t and "Obec:" in t)
    data["location"] = h3.text.replace("Obec:", "").strip() if h3 else "NOT FOUND"
    data["registered"] = soup.select_one('td[headers="sa2"]').text.strip()
    data["envelopes"] = soup.select_one('td[headers="sa3"]').text.strip()
    data["valid"] = soup.select_one('td[headers="sa6"]').text.strip()
    return data

def parse_party_data(soup):
    """získá výsledky hlasování pro jednotlivé strany a pořadí sloupců."""
    parties = {}
    order = []

    #tabulka 1
    party_names1 = soup.select('td[headers="t1sa1 t1sb2"]')
    party_votes1 = soup.select('td[headers="t1sa2 t1sb3"]')

    #tabulka 2
    party_names2 = soup.select('td[headers="t2sa1 t2sb2"]')
    party_votes2 = soup.select('td[headers="t2sa2 t2sb3"]')

    #spojí obě tabulky
    all_names = party_names1 + party_names2
    all_votes = party_votes1 + party_votes2

    for name, vote in zip(all_names, all_votes):
        party = name.text.strip()
        parties[party] = vote.text.strip()
        order.append(party)

    return parties, order

def extract_municipality(code, url):
    """zpracuje jednu obec a vrátí data včetně výsledků stran."""
    soup = fetch_html(url)
    info = parse_general_info(soup)
    info["code"] = code
    party_results, party_order = parse_party_data(soup)
    info.update(party_results)
    return info, party_order

def write_csv(data, parties_order, output_file):
    """zapíše výsledky do CSV souboru s pořadím sloupců podle stran."""
    header = ["code", "location", "registered", "envelopes", "valid"] + parties_order
    with open(output_file, mode="w", newline="", encoding="windows-1250") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

def scrape_election_results(start_url, output_file):
    """hlavní funkce pro stažení výsledků všech obcí a uložení do CSV."""
    print("Checking URL and file name")
    print(f"Fetching data from: {start_url}")

    municipality_links = collect_municipality_urls(start_url)
    all_data = []
    parties_order = None

    for code, url in municipality_links:
        result, order = extract_municipality(code, url)
        all_data.append(result)

        if parties_order is None:
            parties_order = order

    write_csv(all_data, parties_order, output_file)

    print(f"Saved results to '{output_file}'.")
    print("CLOSING main.py")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <URL> <output.csv>")
        sys.exit(1)

    input_url = sys.argv[1]
    output_csv = sys.argv[2]
    scrape_election_results(input_url, output_csv)
