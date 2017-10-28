# -*- coding: utf-8 -*-

from model.image import Image
import mysql.connector as MySQL

HOST = 'localhost'
USER = 'appuser'
PASS = 'ms987654'
DB = 'adi6_db'

class ImageControl:
    def __init__(self):
        self.__con = MySQL.connect(user=USER, password=PASS, host=HOST, database=DB)
        self.__cursor = self.__con.cursor()

    def getImages(self):
        lista = []
        try:
            self.__cursor.execute("SELECT * FROM Image")
            results = self.__cursor.fetchall()
            for row in results:
                print(row)
                #image = Image(row)
        except MySQL.Error as err:
            print(err)
