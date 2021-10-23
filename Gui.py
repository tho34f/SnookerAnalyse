# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 07:01:38 2021

@author: thorb
"""
from tkinter import Label, Button, LabelFrame, Entry, Menu
from PIL import ImageTk, Image
import Konstanten


class Gui:
    """ Gui-KLasse"""

    def __init__(self, master, title):
        self.master = master
        master.title(title)
        # Frames
        self.frameSelection = LabelFrame(master, text="Einleitung", padx=10, pady=10)
        self.frameSpieler = LabelFrame(master, text="Spielereingabe", padx=10, pady=10)
        self.frameTunier = LabelFrame(master, text="Turniereingabe", padx=10, pady=10)
        self.frameDatenbank = LabelFrame(master, text="Aktualisierung Datenbank", padx=10, pady=10)
        self.frameSimulation = LabelFrame(master, text="Simulation", padx=10, pady=10)
        # Eingabefelder
        self.tournamentNumberInput = Entry(self.frameTunier, width=75, borderwidth=10)
        # Labels
        self.spieler_label = Label(self.frameSpieler, text=Konstanten.playerInput)
        self.info_label = Label(self.frameSpieler, text="Nun koennen Sie die Simulation Starten!")
        self.selectionLabel = Label(self.frameSelection, text=Konstanten.openingText)
        self.opening_label = Label(self.frameTunier, text=Konstanten.simulationOpening)
        self.tournament_label = Label(self.frameTunier, text=Konstanten.turnierSelection)
        self.enter_label = Label(self.frameTunier, text=Konstanten.confirmButton)
        self.database_label = Label(self.frameDatenbank, text=Konstanten.databaseActual)
        # Menü
        self.menu = Menu(master)
        self.filemenu = Menu(self.menu)
        self.ranglistenmenu = Menu(self.menu)
        master.config(menu=self.menu)
        self.menu.add_cascade(label="Datei", menu=self.filemenu)
        self.menu.add_cascade(label="Bearbeiten", menu=self.ranglistenmenu)
