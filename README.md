# Engeto_treti_projekt - Volby Scraper

Tento projekt stahuje výsledky voleb z webu [volby.cz](https://www.volby.cz) pro zadaný územní celek (okres, město, obec) a ukládá je do CSV souboru.

## Instalace

1. Vytvoř virtuální prostředí:
   
<img width="328" height="61" alt="image" src="https://github.com/user-attachments/assets/5223cc0c-383f-47d3-9146-b57747905336" />

3. Aktivuj prostředí:
Windows: venv\Scripts\activate
Linux/Mac: source venv/bin/activate

4. Nainstaluj potřebné knihovny:
   
   <img width="537" height="75" alt="image" src="https://github.com/user-attachments/assets/659d7d4f-2643-45b6-9230-33102f1ec15a" />
 
## Spuštění projektu
Projekt spouštíš pomocí 2 argumentů:

<img width="549" height="75" alt="image" src="https://github.com/user-attachments/assets/7d169c1b-0739-40ce-9d84-66fef6ad9409" />

## Příklad
-- python main.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101 vysledky_benesov.csv

Po dokončení bude výstupní CSV soubor obsahovat všechny obce, počty voličů, vydané obálky, platné hlasy a hlasy pro jednotlivé strany.

## Poznámky
Soubor CSV je kódován v UTF-8. Pokud otevřeš soubor v LibreOffice a diakritika nevypadá správně, při otevření vyber kódování UTF-8.
Program nevyžaduje žádný interaktivní vstup, všechna data zadáváš pomocí argumentů při spuštění.
