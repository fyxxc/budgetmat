import sqlite3
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import os


def datenbank_verbinden():
    """Erstellt Verbindung zur Datenbank und die benötigte Tabelle"""
    verbindung = sqlite3.connect('budgetmat_datenbank.db')
    cursor = verbindung.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ausgaben (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kategorie TEXT,
            betrag REAL,
            beschreibung TEXT
        )
    ''')
    verbindung.commit()
    return verbindung, cursor


def ausgabe_hinzufuegen(cursor, verbindung):
    """Neue Ausgabe erfassen und speichern"""
    print("\n--- Neue Ausgabe erfassen ---")
    
    kategorie = input("Kategorie (z.B. Essen, Transport): ")
    betrag_eingabe = input("Betrag in CHF (z.B. 12.50): ")
    
    # Prüfe ob Betrag gültig ist (nur Zahlen und Punkt)
    if re.match(r'^\d+(\.\d+)?$', betrag_eingabe):
        betrag = float(betrag_eingabe)
        beschreibung = input("Beschreibung: ")
        
        cursor.execute(
            'INSERT INTO ausgaben (kategorie, betrag, beschreibung) VALUES (?, ?, ?)',
            (kategorie, betrag, beschreibung)
        )
        verbindung.commit()
        print(f"✓ Ausgabe von {betrag} CHF wurde gespeichert!\n")
    else:
        print("❌ Ungültiger Betrag! Bitte nur Zahlen eingeben (z.B. 25 oder 12.50)\n")


def alle_ausgaben_anzeigen(cursor):
    """Zeigt alle gespeicherten Ausgaben an"""
    print("\n--- Alle Ausgaben ---")
    
    cursor.execute('SELECT * FROM ausgaben')
    ausgaben = cursor.fetchall()
    
    if not ausgaben:
        print("Noch keine Ausgaben vorhanden.\n")
        return
    
    for ausgabe in ausgaben:
        print(f"ID {ausgabe[0]}: {ausgabe[1]} - {ausgabe[2]} CHF - {ausgabe[3]}")
    print()


def gesamtsumme_berechnen(cursor):
    """Berechnet und zeigt die Gesamtsumme aller Ausgaben"""
    print("\n--- Gesamtsumme berechnen ---")
    
    cursor.execute('SELECT SUM(betrag) FROM ausgaben')
    summe = cursor.fetchone()[0]
    
    if summe is None:
        print("Noch keine Ausgaben vorhanden.\n")
    else:
        print(f"Gesamtsumme aller Ausgaben: {summe:.2f} CHF\n")


def grafik_erstellen(cursor):
    """Erstellt ein Balkendiagramm der Ausgaben nach Kategorie und speichert es als PDF"""
    print("\n--- Grafik erstellen ---")
    
    cursor.execute('SELECT kategorie, SUM(betrag) FROM ausgaben GROUP BY kategorie')
    daten = cursor.fetchall()
    
    if not daten:
        print("Noch keine Ausgaben vorhanden.\n")
        return
    
    # Daten aufteilen
    kategorien = [zeile[0] for zeile in daten]
    betraege = [zeile[1] for zeile in daten]
    
    # Grafik erstellen
    plt.figure(figsize=(10, 6))
    plt.bar(kategorien, betraege, color='skyblue')
    plt.xlabel('Kategorie')
    plt.ylabel('Betrag (CHF)')
    plt.title('Ausgaben nach Kategorie')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # PDF speichern
    heute = datetime.now().strftime("%Y-%m-%d")
    dateiname = f"Budgetmat_{heute}.pdf"
    
    # Speicherort (aktuelles Verzeichnis)
    plt.savefig(dateiname)
    plt.close()
    
    print(f"✓ PDF wurde gespeichert: {dateiname}\n")


def menue_anzeigen():
    """Zeigt das Hauptmenü an"""
    print("=" * 40)
    print("   AUSGABEN-TRACKER - BUDGETMAT")
    print("=" * 40)
    print("1 - Ausgabe hinzufügen")
    print("2 - Alle Ausgaben anzeigen")
    print("3 - Gesamtsumme berechnen")
    print("4 - Grafik als PDF erstellen")
    print("5 - Programm beenden")
    print("=" * 40)


def hauptprogramm():
    """Hauptprogramm mit Menüsteuerung"""
    print("Willkommen bei Budgetmat!\n")
    
    # Datenbank vorbereiten
    verbindung, cursor = datenbank_verbinden()
    print("Datenbank bereit!\n")
    
    # Hauptschleife
    while True:
        menue_anzeigen()
        wahl = input("\nDeine Wahl (1-5): ")
        
        if wahl == "1":
            ausgabe_hinzufuegen(cursor, verbindung)
        
        elif wahl == "2":
            alle_ausgaben_anzeigen(cursor)
        
        elif wahl == "3":
            gesamtsumme_berechnen(cursor)
        
        elif wahl == "4":
            grafik_erstellen(cursor)
        
        elif wahl == "5":
            print("\nProgramm wird beendet. Tschüss!")
            verbindung.close()
            break
        
        else:
            print("\n❌ Ungültige Eingabe! Bitte wähle eine Zahl zwischen 1 und 5.\n")


# Programm starten
if __name__ == "__main__":
    hauptprogramm()