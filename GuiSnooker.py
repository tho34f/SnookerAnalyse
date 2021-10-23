# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 17:15:07 2020

@author: thorb
"""

from tkinter import Tk, Label, Button, END, messagebox
import GuiService
import Konstanten
import Gui
import DatenModell

# Ein Fenster und Den Fenstertitle erstellen
fenster = Tk()
snooker_gui = Gui.Gui(fenster, "Snooker-Simulation")
snooker_gui.frameSelection.pack(padx=10, pady=10)

# Datenmodell erzeugen
daten_modell = DatenModell.Daten()


class GuiSnookerClass:
    """ Klasse für bessere Organisation"""

    playerNumber = 0
    roundnumber = 0
    tournamentnumber = 0

    def __init__(self):
        self.tournamentNumberAsInt = int(snooker_gui.tournamentNumberInput.get())
        self.tournamentNumberAsString = snooker_gui.tournamentNumberInput.get()
        self.wahrscheinlichkeiten = []
        self.provisional = []
        self.centurieBreaks = []
        self.spieler = []
        self.resultPlayers = []
        self.resultTournaments = []
        self.worldranking = []
        self.provisionalranking = []
        GuiService.textdatei(self.worldranking, daten_modell.soup_1, "Textdateien/Daten_Weltrangliste.txt")
        GuiService.textdatei(self.provisionalranking, daten_modell.soup_2, "Textdateien/Daten_Provisional.txt")
        self.playerLeft = []

    def fillWithDataFromDb(self):
        """ Datenbankverbindung und Daten besorgen """
        dbPlayers = daten_modell.connectionDb.cursor()
        dbPlayers.execute(Konstanten.selectPlayers)
        self.resultPlayers = dbPlayers.fetchall()
        dbPlayers.execute("SELECT * FROM tournament WHERE id =" + self.tournamentNumberAsString)
        self.resultTournaments = dbPlayers.fetchall()
        dbPlayers.close()
        self.playerNumber = int((self.resultTournaments[0])[2])
        self.roundnumber = int((self.resultTournaments[0])[3])
        self.tournamentnumber = float((self.resultTournaments[0])[4])


def button_action():
    """ Die folgenden Funktionen sollen ausgeführt werden, wenn der Benutzer den Button anklickt """
    snooker_gui.frameSpieler.pack(padx=10, pady=10)

    global gui
    gui = GuiSnookerClass()

    # check, if tournement is corect
    if gui.tournamentNumberAsInt > 24:
        messagebox.showinfo("Information", Konstanten.errorTournament)
        fenster.destroy()
    else:
        gui.fillWithDataFromDb()
        eingabe = Label(snooker_gui.frameSpieler, text="Es wurde das folgende Turnier ausgesucht: " + str((gui.resultTournaments[0])[1]))
        eingabe.grid(row=7, column=0, columnspan=10, padx=100)
        snooker_gui.tournamentNumberInput.delete(0, END)

    snooker_gui.spieler_label.grid(row=8, column=0, columnspan=10, padx=100)

    indexPlayer = 0
    indexRow = 11
    indexColumn = 0
    playerButtons = []
    for data in gui.resultPlayers:
        playerButtons.append(Button(snooker_gui.frameSpieler, text=str(data[1]) + " " + str(data[2])))
        playerButtons[indexPlayer].bind('<Button>', lambda event, temp=data: spieler_action(int(temp[3]), float(temp[5]), int(temp[4]), int(temp[6])))
        playerButtons[indexPlayer].grid(row=indexRow, column=indexColumn, padx=25)
        indexPlayer = indexPlayer + 1
        indexColumn = indexColumn + 1
        if indexColumn % 9 == 0:
            indexColumn = 0
            indexRow = indexRow + 1


def spieler_action(number_1, number_2, number_3, number_4):
    """ Prüft, welche Spieler eingegeben sind und wann Simulation gestartetv werden kann. """
    if len(gui.spieler) <= gui.playerNumber:
        gui.spieler.append(int(number_1))
        gui.wahrscheinlichkeiten.append(float(number_2))
        gui.provisional.append(int(number_3))
        gui.centurieBreaks.append(int(number_4))
        spieler_eingabe = Label(snooker_gui.frameSpieler, text="Es wurde der folgende Spieler eingegeben:" + str(number_1))
        spieler_eingabe.grid(row=24, column=0, columnspan=10, padx=100)
    if len(gui.spieler) == gui.playerNumber:
        spieler_eingabe = Label(snooker_gui.frameSpieler, text="Es wurden genuegend Spieler Eingegeben!")
        spieler_eingabe.grid(row=25, column=0, columnspan=10, padx=100)
        snooker_gui.info_label.grid(row=26, column=0, columnspan=10, padx=10)
        count_button = Button(snooker_gui.frameSpieler, text="Simulation Starten!", command=simulation)
        count_button.grid(row=27, column=0, columnspan=10, padx=100)
    if len(gui.spieler) > gui.playerNumber:
        messagebox.showinfo("Information", Konstanten.enoughtPlayers)


def simulation():
    """ Führt die Simulation des ausgewählten Turniers durch """
    counterPlayernumber = gui.playerNumber
    for g in range(gui.roundnumber):
        counterPlayernumber = (1/2)*counterPlayernumber
        a = 0
        for j in range(int(counterPlayernumber)):
            a = a + 1
            if gui.spieler[2*j] != 0 and gui.spieler[j+a] != 0 and gui.provisional[2*j] != 0 and gui.provisional[j+a] != 0:
                q = GuiService.wahrscheinlichkeitEins(gui, j, 0)
                p = GuiService.wahrscheinlichkeitZwei(gui, j, a, 0)
            else:
                q = GuiService.wahrscheinlichkeitEins(gui, j, 281)
                p = GuiService.wahrscheinlichkeitZwei(gui, j, a, 281)

            if q < p:
                gui.spieler[j] = gui.spieler[j+a]
                gui.wahrscheinlichkeiten[j] = gui.wahrscheinlichkeiten[j+a]
                gui.provisional[j] = gui.provisional[j+a]
                gui.centurieBreaks[j] = gui.centurieBreaks[j + a]
            else:
                gui.spieler[j] = gui.spieler[2*j]
                gui.wahrscheinlichkeiten[j] = gui.wahrscheinlichkeiten[2*j]
                gui.provisional[j] = gui.provisional[2*j]
                gui.centurieBreaks[j] = gui.centurieBreaks[2*j]
    snooker_gui.frameSimulation.pack(padx=10, pady=10)
    ergebniss = Label(snooker_gui.frameSimulation, text="Gewinner des Turniers ist:" + str(gui.spieler[0]))
    ergebniss.grid(row=28, column=0, columnspan=10, padx=100)
    button_quit = Button(snooker_gui.frameSimulation, text="Programm beenden!", command=shutdown)
    button_quit.grid(row=29, column=0, columnspan=10, padx=100)


def shutdown():
    """ Schließt das Fenster """
    fenster.destroy()


def undo():
    """ Letzter Schritt wird rückgängig gemacht """
    länge = len(gui.spieler)
    gui.spieler.remove(gui.spieler[länge-1])
    gui.wahrscheinlichkeiten.remove(gui.wahrscheinlichkeiten[länge-1])
    gui.provisional.remove(gui.provisional[länge-1])
    gui.centurieBreaks.remove(gui.centurieBreaks[länge-1])


def simulation_schreiben():
    """ Schreibt das Ergebniss der SImulation in eine Textdatei """
    file = open("Textdateien/Snooker_Simulation.txt", "w")
    file.write("Turniergewicht:" + str(gui.tournamentnumber) + "\n")
    file.write("Spielerzahl:" + str(gui.playerNumber) + "\n")
    file.write("Teilnehmende Spieler:")
    file.write(",".join((map(str, gui.spieler))) + "\n")
    file.write("Gewinnwahrscheinlichkeiten:")
    file.write(",".join((map(str, gui.wahrscheinlichkeiten))) + "\n")
    file.write("Position Provisional Ranking:")
    file.write(",".join((map(str, gui.provisional))) + "\n")
    file.write("Anzahl der Centurie Breaks:")
    file.write(",".join((map(str, gui.centurieBreaks))))
    file.close()


def datenbank_selection():
    """ Datenbank soll aktualisiert werden """
    snooker_gui.frameDatenbank.pack(padx=10, pady=10)
    leftPlayers_button = Button(snooker_gui.frameDatenbank, text="Fehlende Spieler", command=left_players_action)
    actualData_button = Button(snooker_gui.frameDatenbank, text="Vorhandene Daten aktualisieren", command=actual_datata_action)
    snooker_gui.database_label.grid(row=2, column=0, columnspan=10, padx=100)
    leftPlayers_button.grid(row=3, column=1, columnspan=5, padx=100)
    actualData_button.grid(row=3, column=4, columnspan=10, padx=100)


def left_players_action():
    """Ergänzt fehlende Spiler in der Datenbank"""
    playerRankingWstLastName = []
    for i in range(0, 127):
        playerRankingWstLastName.append(gui.worldranking[3*i+1])
        playerLastName = str(playerRankingWstLastName[i]).split(" ")[1]
        playerRankingWstLastName[i] = playerLastName
    dbPlayers = daten_modell.connectionDb.cursor()
    dbPlayers.execute(Konstanten.selectPlayers)
    resultPlayers = dbPlayers.fetchall()
    for i in range(0, 127):
        isPlayerLeft = 0
        for data in resultPlayers:
            temp = data
            if temp[2] == playerRankingWstLastName[i]:
                isPlayerLeft = isPlayerLeft + 1
        if isPlayerLeft != 1:
            gui.playerLeft.append(playerRankingWstLastName[i])
    dbPlayers.close()


def actual_datata_action():
    """Aktualisiert Datenschätze in der Datenbank"""
    dbPlayers = daten_modell.connectionDb.cursor()
    dbPlayers.execute(Konstanten.selectPlayers)
    dbPlayers.close()


def simulation_selection():
    """ Einleitung, wenn Simulation ausgewählt wurde """
    snooker_gui.frameTunier.pack(padx=10, pady=10)
    # Buttons bzw. Labels erstellen und Komponenten im Fenster in der gwünschten Reihenfolge hinzufügen
    confirm_button = Button(snooker_gui.frameTunier, text="Ok", command=button_action)

    snooker_gui.opening_label.grid(row=2, column=0, columnspan=10, padx=100)
    snooker_gui.tournament_label.grid(row=3, column=0, columnspan=10, padx=100)
    snooker_gui.tournamentNumberInput.grid(row=4, column=0, columnspan=10, padx=100)
    snooker_gui.enter_label.grid(row=5, column=0, columnspan=10, padx=100)
    confirm_button.grid(row=6, column=0, columnspan=10, padx=100)


# Ein Menü erstellen
snooker_gui.filemenu.add_command(label="Rückgängig", command=undo)
snooker_gui.filemenu.add_separator()
snooker_gui.filemenu.add_command(label=Konstanten.writeSimulation, command=simulation_schreiben)
snooker_gui.filemenu.add_separator()
snooker_gui.filemenu.add_command(label="Programm beenden", command=shutdown)
snooker_gui.ranglistenmenu.add_command(label="1-Jahres-Rangliste Plotten", command=lambda: GuiService.plotten(gui.provisionalranking, "Provisional Ranking", "Preisgeld", "Spieler"))
snooker_gui.ranglistenmenu.add_command(label="Weltrangliste Plotten", command=lambda: GuiService.plotten(gui.worldranking, "Weltrangliste", "Preisgeld", "Spieler"))

snooker_gui.selectionLabel.grid(row=0, column=0, columnspan=10, padx=100)
selectionSimulationButton = Button(snooker_gui.frameSelection, text="Simulation durchführen", command=simulation_selection)
selectionSimulationButton.grid(row=1, column=1, columnspan=5, padx=100)
selectionDatenbankButton = Button(snooker_gui.frameSelection, text="Datenbank aktuallisieren", command=datenbank_selection)
selectionDatenbankButton.grid(row=1, column=4, columnspan=10, padx=100)


# In der Ereignisschleife auf Eingabe des Benutzers warten.
fenster.geometry("1920x1080")
fenster.mainloop()
