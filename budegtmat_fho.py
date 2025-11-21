import sqlite3
import re
import matplotlib
matplotlib.use('Agg')  # Backend ohne GUI
import matplotlib.pyplot as plt
from datetime import datetime
import os

# === SCHRITT 1: Datenbank erstellen ===
print("Starte Budgetmat...")

# Verbindung zur Datenbank herstellen (wird automatisch erstellt)
verbindung = sqlite3.connect('ausgaben.db')
cursor = verbindung.cursor()

# Tabelle erstellen
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ausgaben (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kategorie TEXT,
        betrag REAL,
        beschreibung TEXT
    )
''')
verbindung.commit()
print("Datenbank bereit!\n")


# === SCHRITT 2: Hauptprogramm ===
while True:
    print("--- AUSGABEN-TRACKER ---")
    print("1 = Ausgabe hinzufügen")
    print("2 = Alle Ausgaben anzeigen")
    print("3 = Summe berechnen")
    print("4 = Grafik erstellen und als PDF speichern")
    print("5 = Beenden")
    
    # Eingabe vom Benutzer
    wahl = input("\nWas möchtest du tun? ")
    
    
    # === OPTION 1: Ausgabe hinzufügen ===
    if wahl == "1":
        print("\n--- Neue Ausgabe ---")
        
        # Kategorie eingeben
        kategorie = input("Kategorie (z.B. Essen, Transport): ")
        
        # Betrag eingeben und mit Regex prüfen
        betrag_eingabe = input("Betrag (z.B. 12.50): ")
        
        # Regex: Prüft ob nur Zahlen und optional ein Punkt mit Dezimalstellen
        if re.match(r'^\d+(\.\d+)?$', betrag_eingabe):
            betrag = float(betrag_eingabe)
            
            # Beschreibung eingeben
            beschreibung = input("Beschreibung: ")
            
            # In Datenbank speichern
            cursor.execute('INSERT INTO ausgaben (kategorie, betrag, beschreibung) VALUES (?, ?, ?)', 
                          (kategorie, betrag, beschreibung))
            verbindung.commit()
            
            print(f"✓ Ausgabe von {betrag}CHF gespeichert!\n")
        else:
            print("Ungültiger Betrag! Bitte nur Zahlen eingeben.\n")
    
    
    # === OPTION 2: Alle Ausgaben anzeigen ===
    elif wahl == "2":
        print("\n--- Alle Ausgaben ---")
        
        # Daten aus Datenbank auslesen
        cursor.execute('SELECT * FROM ausgaben')
        alle_ausgaben = cursor.fetchall()
        
        # Prüfen ob Ausgaben vorhanden sind
        if len(alle_ausgaben) == 0:
            print("Noch keine Ausgaben vorhanden.\n")
        else:
            # Alle Ausgaben durchgehen und anzeigen
            for ausgabe in alle_ausgaben:
                id_nummer = ausgabe[0]
                kategorie = ausgabe[1]
                betrag = ausgabe[2]
                beschreibung = ausgabe[3]
                
                print(f"ID {id_nummer}: {kategorie} - {betrag}€ - {beschreibung}")
            print()
    
    
    # === OPTION 3: Summe berechnen ===
    elif wahl == "3":
        print("\n--- Gesamtsumme ---")
        
        # Summe aus Datenbank berechnen
        cursor.execute('SELECT SUM(betrag) FROM ausgaben')
        summe = cursor.fetchone()[0]
        
        # Prüfen ob Summe existiert
        if summe is None:
            print("Noch keine Ausgaben vorhanden.\n")
        else:
            print(f"Gesamtsumme: {summe} CHF\n")
    
    
    # === OPTION 4: Grafik erstellen ===
    elif wahl == "4":
        print("\n--- Grafik erstellen ---")
        
        # Daten aus Datenbank auslesen
        cursor.execute('SELECT kategorie, SUM(betrag) FROM ausgaben GROUP BY kategorie')
        daten = cursor.fetchall()
        
        # Prüfen ob Ausgaben vorhanden sind
        if len(daten) == 0:
            print("Noch keine Ausgaben vorhanden.\n")
        else:
            # Kategorien und Beträge trennen
            kategorien = []
            betraege = []
            
            for zeile in daten:
                kategorien.append(zeile[0])
                betraege.append(zeile[1])
            
            # Grafik erstellen
            plt.figure(figsize=(10, 6))
            plt.bar(kategorien, betraege, color='skyblue')
            plt.xlabel('Kategorie')
            plt.ylabel('Betrag (CHF)')
            plt.title('Ausgaben nach Kategorie')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # Dateiname mit aktuellem Datum erstellen
            heute = datetime.now().strftime("%Y-%m-%d")
            dateiname = f"Budgetmat_fho_{heute}.pdf"
            
            # Als PDF im angegebenen Ordner speichern
            ordner = "/Users/fynnhofmann/Documents/GitHub/BBZ-CFP/122-ICT/py/budgetmat"
            vollstaendiger_pfad = os.path.join(ordner, dateiname)
            plt.savefig(vollstaendiger_pfad)
            plt.close()
            
            print(f"Grafik gespeichert: {dateiname}\n")
    
    
    # === OPTION 5: Beenden ===
    elif wahl == "5":
        print("\nTschüss!")
        verbindung.close()
        break
    
    
    # === Ungültige Eingabe ===
    else:
        print("\nUngültige Eingabe! Bitte 1, 2, 3, 4 oder 5 wählen.\n")