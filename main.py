"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Tomáš Polický
email: policky.t@gmail.com
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import csv
import re

def stahni_stranku(url):
    """Stáhne stránku a vrátí BeautifulSoup objekt."""
    response = requests.get(url)
    response.encoding = "iso-8859-2"
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def najdi_odkazy_na_obce(soup, base="https://www.volby.cz/pls/ps2017nss/"):
    """
    Vrací seznam dvojic (kod_obce, plna_url)
    """
    results = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "xobec=" in href or "ps311" in href:
            full = urljoin(base, href)
            # extrahuj parametr xobec z URL
            parsed = urlparse(full)
            qs = parse_qs(parsed.query)
            kod = None
            if "xobec" in qs:
                kod = qs["xobec"][0]
            elif a.get_text(strip=True).isdigit():
                kod = a.get_text(strip=True)
            else:
                # fallback: poslední číslo v href
                import re
                m = re.search(r"(\\d{5,7})", href)
                kod = m.group(1) if m else href
            results.append((kod, full))
    # odstranit duplicity při zachování pořadí
    seen = set(); uniq=[]
    for k,u in results:
        key = (k,u)
        if key not in seen:
            seen.add(key); uniq.append((k,u))
    return uniq

def parsuj_obec(soup, kod_obce):
    """
    Z detailní stránky obce vytáhne název, počty voličů a hlasy pro jednotlivé strany.
    Vrací slovník s daty pro jednu obec.
    """
    zaznam = {"kod": kod_obce}

    # === 1) Název obce ===
    h3 = soup.find("h3")
    if h3:
        zaznam["nazev"] = h3.get_text(strip=True)
    else:
        # fallback – pokud h3 chybí, zkus title
        title = soup.find("title")
        zaznam["nazev"] = title.get_text(strip=True).split(" - ")[0] if title else "Neznámá"

    # === 2) Počty voličů, vydané obálky, platné hlasy ===
    for tr in soup.find_all("tr"):
        td = tr.find_all("td")
        if len(td) >= 2:
            nadpis = td[0].get_text(strip=True)
            hodnota = td[1].get_text(strip=True).replace("\xa0", "").replace(" ", "").replace(",", ".")
            try:
                hodnota_int = int(float(hodnota))
            except ValueError:
                hodnota_int = 0

            if "Voliči v seznamu" in nadpis:
                zaznam["volici"] = hodnota_int
            elif "Vydané obálky" in nadpis:
                zaznam["vydane_obalky"] = hodnota_int
            elif "Platné hlasy" in nadpis:
                zaznam["platne_hlasy"] = hodnota_int

    # nastav výchozí hodnoty, pokud se něco nenašlo
    for klic in ["volici", "vydane_obalky", "platne_hlasy"]:
        zaznam.setdefault(klic, 0)

    # === 3) Hlasy pro jednotlivé strany ===
    zaznam_stran = {}
    for tr in soup.find_all("tr"):
        bunky = tr.find_all("td")
        if len(bunky) >= 3 and bunky[0].get_text(strip=True).isdigit():
            nazev_strany = bunky[1].get_text(strip=True)
            hlas_text = bunky[2].get_text(strip=True).replace("\xa0", "").replace(" ", "").replace(",", ".")
            try:
                hlasy = int(float(hlas_text))
            except ValueError:
                hlasy = 0
            zaznam_stran[nazev_strany] = hlasy

    zaznam.update(zaznam_stran)
    return zaznam

def uloz_do_csv(vsechny_zaznamy, vsechny_strany, nazev_souboru):
    """
    Zapíše výsledky do CSV se všemi stranami jako sloupce.
    Kódování UTF-8 zajistí správné zobrazení českých znaků.
    """
    hlavicka = ["kod", "nazev", "volici", "vydane_obalky", "platne_hlasy"] + sorted(vsechny_strany)

    with open(nazev_souboru, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=hlavicka)
        writer.writeheader()

        for radek in vsechny_zaznamy:
            for s in vsechny_strany:
                radek.setdefault(s, 0)
            writer.writerow(radek)


def main(url_okresu, nazev_csv):
    soup_hlavni = stahni_stranku(url_okresu)
    odkazy_na_obce = najdi_odkazy_na_obce(soup_hlavni)

    vsechny_zaznamy = []
    vsechny_strany = set()

    for kod_obce, url_obce in odkazy_na_obce:
        try:
            soup_obce = stahni_stranku(url_obce)
        except requests.RequestException as e:
            print(f"Chyba při stahování obce {kod_obce}: {e}")
            continue

        zaznam = parsuj_obec(soup_obce, kod_obce)
        vsechny_zaznamy.append(zaznam)

        # uložíme názvy stran (vše kromě základních údajů)
        vsechny_strany.update([k for k in zaznam.keys() if k not in ["kod","nazev","volici","vydane_obalky","platne_hlasy"]])

    uloz_do_csv(vsechny_zaznamy, vsechny_strany, nazev_csv)


if __name__ == "__main__":
    import sys

    # kontrola, že má uživatel správný počet argumentů
    if len(sys.argv) != 3:
        print("Chyba: Zadej 2 argumenty – URL a název výstupního souboru.")
        print("Např.: python main.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101 vysledky_benesov.csv")
        sys.exit(1)

    url_okresu = sys.argv[1]
    nazev_csv = sys.argv[2]

    # kontrola, že URL vypadá správně
    if "volby.cz" not in url_okresu or "ps32" not in url_okresu:
        print("Chyba: první argument musí být platná URL na stránku okresu (např. ps32...).")
        sys.exit(1)

    print("Stahuji data, prosím o trpělivost...")
    main(url_okresu, nazev_csv)
    print(f"Hotovo! Výsledky byly uloženy do souboru {nazev_csv}.")