import sqlite3
import re

print("Programm wird gestartet...")

# --- KRITERIUM: SQLITE3 (DB erstellen) ---
# Wir verbinden uns zur Datenbank (oder erstellen sie, falls sie nicht existiert)
verbindung = sqlite3.connect('db_budgetmat_fho.db')
cursor = verbindung.cursor()

# Tabelle erstellen (nur wenn sie noch nicht da ist)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ausgaben (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        zweck TEXT,
        betrag REAL
    )
''')
verbindung.commit() # Speichern nicht vergessen!


# --- KRITERIUM: KONTROLLSTRUKTUREN (while-Schleife) ---
while True:
    print("\n--- MENÜ ---")
    print("1: Neue Ausgabe eintragen")
    print("2: Alle Ausgaben ansehen")
    print("3: Beenden")
    
    # --- KRITERIUM: EIN- UND AUSGABEN (input) ---
    auswahl = input("Deine Wahl: ")
    
    # --- KRITERIUM: KONTROLLSTRUKTUREN (if/elif) ---
    if auswahl == "1":
        print("\n-- Eintrag --")
        zweck = input("Wofür war das Geld? ")
        zahl_string = input("Wie viel hat es gekostet(z.B. 15.50)? ")
        
        # --- KRITERIUM: REGEX ---
        # Wir prüfen: Startet mit Zahl(en), optional ein Punkt, optional mehr Zahlen
        if re.match(r'^\d+(\.\d+)?$', zahl_string):
            
            # Umwandeln in Kommazahl
            betrag = float(zahl_string)
            
            # --- KRITERIUM: SQLITE3 (Daten einfügen) ---
            cursor.execute("INSERT INTO ausgaben (zweck, betrag) VALUES (?, ?)", (zweck, betrag))
            verbindung.commit()
            print("Gespeichert!")
            
        else:
            print("FEHLER: Das war keine gültige Zahl (bitte Punkt statt Komma nutzen).")
            
    elif auswahl == "2":
        print("\n-- Liste --")
        
        # --- KRITERIUM: SQLITE3 (Daten auslesen) ---
        cursor.execute("SELECT * FROM ausgaben")
        alle_daten = cursor.fetchall()
        
        # --- KRITERIUM: KONTROLLSTRUKTUREN (for-Schleife) ---
        for zeile in alle_daten:
            # zeile ist ein Tupel, z.B. (1, 'Essen', 12.50)
            print(f"ID: {zeile[0]} | Zweck: {zeile[1]} | Betrag: {zeile[2]} CHF")
            
    elif auswahl == "3":
        print("Tschüss!")
        verbindung.close() # Sauber schließen
        break # Schleife beenden
        
    else:
        print("Ungültige Eingabe.")