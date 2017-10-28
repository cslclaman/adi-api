# -*- coding: utf-8 -*-

from model.image import Image
import mysql.connector as MySQL

HOST = 'localhost'
USER = 'appuser'
PASS = 'ms987654'
DB = 'adi6_db'

LIMIT = 25

class ImageControl:
    def __init__(self):
        self.__con = MySQL.connect(user=USER, password=PASS, host=HOST, database=DB)
        self.__cursor = self.__con.cursor()

    def get_image_list(self, pagenum, tags):
        listImages = []
        try:
            page = (pagenum - 1) * LIMIT
            query = "SELECT * FROM Image WHERE tag_string like \'{0}\' LIMIT {1},{2}".format(("%"+tags+"%"),page,LIMIT)
            self.__cursor.execute(query)
            results = self.__cursor.fetchall()
            for row in results:
                image = Image(row)
                listImages.append(image)
        except MySQL.Error as err:
            print(err)

        return listImages;
