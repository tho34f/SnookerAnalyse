# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 07:10:07 2021

@author: thorb
"""

import matplotlib.pyplot as plt
import math
from bs4 import BeautifulSoup
import requests


def plotten(array_3, titel, xAchse, yAchse):
    array_1 = []
    array_2 = []
    for i in range(0, 127):
        array_1.append(array_3[3*i])
        array_1[i] = int(array_1[i])
        array_2.append(array_3[3*i+2])
        array_2[i] = array_2[i].replace(",", "")
        array_2[i] = int(array_2[i])
    plt.plot(array_1, array_2, markersize=5, linewidth=2,)
    plt.title(titel)
    plt.ylabel(yAchse, size="x-large")
    plt.xlabel(xAchse, size="x-large")
    plt.show()


def textdatei(matrix_2, data, titel):
    matrix_1 = data.find_all('td')
    write(titel, matrix_1, matrix_2)


def write(titel, rangliste, array):
    file = open(titel, "w")
    for spieler in rangliste:
        # print(spieler.text)
        array.append(spieler.text)
        file.write(spieler.text)
        file.write("\n")
    file.close()


def getSoup(adresse):
    r = requests.get(adresse)
    return BeautifulSoup(r.text, "html.parser")


def wahrscheinlichkeitEins(gui, j, fallback):
    helpW = gui.wahrscheinlichkeiten[2*j] + math.log(math.log(gui.centurieBreaks[2*j] + 2), 10)
    if fallback > 0:
        return (gui.tournamentnumber/(math.log(fallback)))*helpW
    else:
        return (gui.tournamentnumber/(math.log(gui.spieler[2*j] + gui.provisional[2*j] + 1)))*helpW


def wahrscheinlichkeitZwei(gui, j, a, fallback):
    helpW = (gui.wahrscheinlichkeiten[j+a] + math.log(math.log(gui.centurieBreaks[j + a] + 2), 10))
    if fallback > 0:
        return (gui.tournamentnumber/(math.log(281)))*helpW
    else:
        return(gui.tournamentnumber/(math.log(gui.spieler[j+a] + gui.provisional[j+a] + 1)))*helpW
