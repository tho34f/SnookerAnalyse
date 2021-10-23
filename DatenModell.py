# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 17:53:26 2021

@author: thorb
"""
import mysql
import mysql.connector
import GuiService


class Daten:

    def __init__(self):
        # Datenbankverbindung
        self.connectionDb = mysql.connector.connect(host="127.0.0.1", user="root", passwd="MaraTeske30031994!", db="snooker")
        self.soup_1 = GuiService.getSoup("https://wst.tv/rankings/world-rankings-2/")
        self.soup_2 = GuiService.getSoup("https://wst.tv/rankings/1-year-ranking-list/")
