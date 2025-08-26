# Ersteller: Noel Backhaus

from random import randint
from hangman_figur import figuren
import string

# Variablen

sprache = ""
modus = ""
wort = ""
eingabe = ""
ratebuchstabe = ""
kleinbuchstabe = " "
grossbuchstabe = " "
ratewort = ""
geheimwort = ""
buchstabenliste = list(string.ascii_lowercase)
fertigergalgen = figuren
galgenindex = 0
galgenkontrolle = False
galgenstand = ""
spielen = True
gewonnen = False
verloren = False
spielende = False

# Farben

class Farben:
    GRUEN = '\033[92m'
    ROT = '\033[91m'
    ENDE = '\033[0m'

# Unterprogramme

def spracheauswaehlen():
    global sprache
    
    # Eingabe
    print("")
    sprache = input("Englisch oder Deutsch? Bitte wählen Sie eine Sprache: ")

    # Plausibilitätskontrolle
    sprache = sprache.lower()
    optionen = ["english", "englisch", "german", "deutsch", "de", "en"]
    while not sprache in optionen:
        print("")
        sprache = input("Ungültige Eingabe. Bitte geben Sie Englisch oder Deutsch ein: ")
        sprache = sprache.lower()
    if sprache == "english" or sprache == "englisch" or sprache == "en":
        sprache = "englisch"
    elif sprache == "german" or sprache == "deutsch" or sprache == "de":
        sprache = "deutsch"

def modusauswaehlen():
    global modus

    # Eingabe
    print("")
    modus = input("1- oder 2-Spielermodus? Bitte geben Sie 1 oder 2 ein: ")

    # Plausibilitätskontrolle
    while modus != "1" and modus != "2":
        print("")
        modus = input("Ungültige Eingabe. Bitte geben Sie 1 oder 2 ein: ")
        
def sonderzeichen_finden():
    global nicht_geduldete_sonderzeichen
    
    alphabet = string.ascii_letters
    geduldete_sonderzeichen = ["Ã", "Ÿ", "„", "–", "œ", "¤", "¶", "¼", "\n"]
    nicht_geduldete_sonderzeichen = []
    
    with open("hangman_deutsch_wortliste.txt", "r") as wortliste:
        for zeile, i in enumerate(wortliste):
            for x in i:
                if not x in alphabet and not x in nicht_geduldete_sonderzeichen and not x in geduldete_sonderzeichen:
                    nicht_geduldete_sonderzeichen += x
    with open("hangman_englisch_wortliste.txt", "r") as wortliste:
        for zeile, i in enumerate(wortliste):
            for x in i:
                if not x in alphabet and not x in nicht_geduldete_sonderzeichen and not x in geduldete_sonderzeichen:
                    nicht_geduldete_sonderzeichen += x
                    
def wortauswaehlen():
    global wort
    global nicht_geduldete_sonderzeichen
    
    # Modus überprüfen
    if modus == "1":
        # deutsches Wort
        if sprache == "deutsch":
            # Zufallsgenerator
            x = randint(1, 239650)
            # Liste auslesen
            with open("hangman_deutsch_wortliste.txt", "r") as wortliste:
                for zeile, i in enumerate(wortliste):
                    if zeile+1 == x and not i in nicht_geduldete_sonderzeichen:
                        wort = i
            # Sonderzeichen ersetzen
            sonderzeichen = ["ÃŸ", "Ã„", "Ã–", "Ãœ", "Ã¤", "Ã¶", "Ã¼"]        #(Umlaute: ß,Ä,Ö,Ü,ä,ö,ü)
            buchstaben = ["ss", "Ae", "Oe", "Ue", "ae", "oe", "ue"]
            for x in range(len(sonderzeichen)):
                wort = wort.replace(sonderzeichen[x], buchstaben[x])
        # englisches Wort
        if sprache == "englisch":
            #Zufallsgenerator
            x = randint(1, 354297)
            #Liste auslesen
            with open("hangman_englisch_wortliste.txt", "r") as wortliste:
                for zeile, i in enumerate(wortliste):
                    if zeile+1 == x and not i in nicht_geduldete_sonderzeichen:
                        wort = i     
        # Leerstellen entfernen
        wort = wort.strip()

def worteingeben():
    global wort
    korrekt = False

    # Modus überprüfen
    if modus == "2":
        # Eingabe des Wortes
        print("")
        wort = input("Bitte geben Sie das gewünschte Wort ein: ")
        # Leerstellen entfernen
        wort = wort.strip()
        
        # Plausibilitätskontrolle
        sonderzeichen = [223, 196, 214, 220, 228, 246, 252]
        while korrekt == False:
            for i in wort:
                x = ord(i)
                if (x >= 65 and x <= 90) or (x >= 97 and x <= 122) or x in sonderzeichen:
                    korrekt = True
                    continue
                else:
                    korrekt = False
                    break
            if korrekt == False:
                print("")
                wort = input("Ungültige Eingabe. Bitte geben Sie ein Wort ein: ")
                # Leerstellen entfernen
                wort = wort.strip()
                
        # Sonderzeichen ersetzen
        sonderzeichen = ["ß", "Ä", "Ö", "Ü", "ä", "ö", "ü"]
        buchstaben = ["ss", "Ae", "Oe", "Ue", "ae", "oe", "ue"]
        for x in range(len(sonderzeichen)):
            wort = wort.replace(sonderzeichen[x], buchstaben[x])

def verschluesseln():
    global geheimwort
    for i in wort:
        geheimwort += "*"

def raten():
    global eingabe
    global ratebuchstabe
    global ratewort
    korrekt = False

    # Eingabe
    eingabe = input("Raten Sie einen Buchstaben oder ein Wort: ")

    # Plausibilitätskontrolle
    while korrekt == False:
        for i in eingabe:
            x = ord(i)
            if (x >= 65 and x <= 90) or (x >= 97 and x <= 122):
                korrekt = True
                continue
            else:
                korrekt = False
                break
        if korrekt == False:
            print("")
            eingabe = input("Ungültige Eingabe. Bitte geben Sie einen Buchstaben oder ein Wort ein: ")

    # Unterscheidung zwischen Wort und Buchstabe
    if len(eingabe) > 1:
        ratewort = eingabe
    if len(eingabe) == 1:
        ratebuchstabe = eingabe   
     
def buchstabeauswerten():
    global kleinbuchstabe
    global grossbuchstabe
    global buchstabenliste
    global galgenindex
    global galgenkontrolle

    # Kontrolle zur Ausführung der Funktion
    if ratebuchstabe == eingabe:
        # Überprüfung ob Buchstabe schon geraten wurde
        if ratebuchstabe.lower() not in buchstabenliste:
            print("")
            print("Der Buchstabe", ratebuchstabe, "wurde schon geraten!")
            galgenkontrolle = False
        else:
            # Umwandlung in Klein- oder Großbuchstabe
            kleinbuchstabe = " "
            grossbuchstabe = " "
            kleinbuchstabe = ratebuchstabe.lower()
            grossbuchstabe = ratebuchstabe.upper()
            # Überprüfung des Buchstabens
            if kleinbuchstabe in wort or grossbuchstabe in wort:
                print("")
                print(Farben.GRUEN + "Gratulation! Der Buchstabe", ratebuchstabe, "ist richtig!" + Farben.ENDE)
                galgenkontrolle = False
            else:
                print("")
                print(Farben.ROT + "Der Buchstabe", ratebuchstabe, "ist falsch!" + Farben.ENDE)
                galgenindex += 1
                galgenkontrolle = True
            # Buchstabe in Liste durch " " ersetzen
            index = buchstabenliste.index(kleinbuchstabe)
            buchstabenliste[index] = "_"

def wortauswerten():
    global geheimwort
    global galgenindex
    global galgenkontrolle
    global gewonnen

    # Kontrolle zur Ausführung der Funktion
    if ratewort == eingabe:
        # Überprüfung des Wortes
        if ratewort == wort:
            print("")
            print(Farben.GRUEN + "Das Wort", ratewort, "ist richtig! Sie haben gewonnen!" + Farben.ENDE)
            geheimwort = wort
            galgenkontrolle = False
            gewonnen = True
        else:
            print("")
            print(Farben.ROT + "Das Wort", ratewort, "ist falsch. Das können Sie besser!" + Farben.ENDE)
            galgenindex += 1
            galgenkontrolle = True

def entschluesseln():
    global geheimwort
    global gewonnen
    hilfswort = ""

    # Kontrolle zur Ausführung der Funktion
    if eingabe == ratebuchstabe:
        # Aktualisierung des aktuellen Stands vom Wort
        x = 0
        for i in wort:
            if i == kleinbuchstabe:
                hilfswort += kleinbuchstabe
            elif i == grossbuchstabe:
                hilfswort += grossbuchstabe
            else:
                hilfswort += geheimwort[x]
            x += 1
        geheimwort = hilfswort

    # Kontrolle des Spielendes
    if geheimwort == wort:
        print("")
        print("Sie haben's geschafft! Sie haben alle Buchstaben erraten!")
        gewonnen = True

def galgen():
    global galgenstand
    global figuren
    global fertigergalgen
    global verloren

    # Kontrolle zur Ausführung der Funktion
    if galgenkontrolle == True:
        galgenstand = fertigergalgen[galgenindex]
        if galgenindex == 7:
            verloren = True

    # Kontrolle des Spielendes
    if verloren == True:
        print("")
        print("Der Galgen ist fertig. Sie haben verloren... ")
        print("")
        print("Das Wort war:", wort)

def rueckmelden():
    global buchstabenliste
    global fertigergalgen
    global gewonnen
    global verloren

    if gewonnen == True or verloren == True:
        print("")
        print("Das ist Ihr finaler Stand: ")
    else:
        print("")
        print("Das ist Ihr aktueller Stand: ")
    print("")
    print("Wort:", geheimwort)
    print("")
    print("Galgen:\n", galgenstand)
    print("Übrige Buchstaben:", " ".join(buchstabenliste))
    print("")


def wiederholen():
    global spielen

    # Eingabe
    abfrage = input("Wollen Sie nochmal spielen? ")
    abfrage = abfrage.lower()
    
    # Plausibilitätskontrolle
    while abfrage != "ja" and abfrage != "nein":
        print("")
        abfrage = input("Ungültige Eingabe. Bitte geben Sie ja oder nein ein: ")

    # Festlegung
    if abfrage == "ja":
        spielen = True
        leeren(100)
        zuruecksetzen()
    elif abfrage == "nein":
        spielen = False

def zuruecksetzen():
    global sprache
    global modus
    global wort
    global eingabe
    global ratebuchstabe
    global kleinbuchstabe
    global grossbuchstabe
    global ratewort
    global geheimwort
    global buchstabenliste
    global fertigergalgen
    global galgenindex
    global galgenkontrolle
    global galgenstand
    global spielen
    global gewonnen
    global verloren

    sprache = ""
    modus = ""
    wort = ""
    eingabe = ""
    ratebuchstabe = ""
    kleinbuchstabe = " "
    grossbuchstabe = " "
    ratewort = ""
    geheimwort = ""
    buchstabenliste = list(string.ascii_lowercase)
    fertigergalgen = figuren
    galgenindex = 0
    galgenkontrolle = False
    galgenstand = ""
    spielen = True
    gewonnen = False
    verloren = False

def leeren(laenge):
    for i in range(laenge):
        print("")
        
# Hauptprogramm

# Vorbereitung
while spielen == True:
    spracheauswaehlen()
    modusauswaehlen()
    sonderzeichen_finden()
    wortauswaehlen()
    worteingeben()
    verschluesseln()
    leeren(200)
    print("Los geht's!")
    rueckmelden()
    # Spielstart
    while gewonnen == False and verloren == False:
        raten()
        leeren(100)
        buchstabeauswerten()
        entschluesseln()
        wortauswerten()
        galgen()
        rueckmelden()
    wiederholen()
    
