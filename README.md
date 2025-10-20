# Engeto_treti_projekt

# Volby Scraper

Tento projekt stahuje výsledky voleb z webu [volby.cz](https://www.volby.cz) pro zadaný územní celek (okres, město, obec) a ukládá je do CSV souboru.

## Instalace

1. Vytvoř virtuální prostředí:
bashpython -m venv venv

2. Aktivuj prostředí:
Windows: venv\Scripts\activate
Linux/Mac: source venv/bin/activate

3. Nainstaluj potřebné knihovny:
pip install -r requirements.txt

## Spuštění projektu
Projekt spouštíš pomocí 2 argumentů:
python main.py <URL_uzemniho_celku> <nazev_vystupniho_souboru.csv>

## Příklad
python main.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101 vysledky_benesov.csv
Po dokončení bude výstupní CSV soubor obsahovat všechny obce, počty voličů, vydané obálky, platné hlasy a hlasy pro jednotlivé strany.

## Poznámky
Soubor CSV je kódován v UTF-8. Pokud otevřeš soubor v LibreOffice a diakritika nevypadá správně, při otevření vyber kódování UTF-8.
Program nevyžaduje žádný interaktivní vstup, všechna data zadáváš pomocí argumentů při spuštění.
