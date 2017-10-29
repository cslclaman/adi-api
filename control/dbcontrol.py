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

    def get_image_list(self, tags, pagenum, limit):
        listImages = []
        try:
            page = (pagenum - 1) * limit
            query = "SELECT * FROM Image WHERE tag_string like \'{0}\' LIMIT {1},{2}".format(("%"+tags+"%"),page,limit)
            self.__cursor.execute(query)
            results = self.__cursor.fetchall()
            for row in results:
                image = Image(row)
                listImages.append(image)
        except MySQL.Error as err:
            print(err)

        return listImages;

    def get_image_by_id(self, id):
        try:
            query = "SELECT * FROM Image WHERE id = {0}".format(id)
            self.__cursor.execute(query)
            row = self.__cursor.fetchone()
            if row is not None:
                return Image(row)
            else:
                return None
        except MySQL.Error as err:
            print(err)
            return None

    def get_image_by_md5(self, md5):
        try:
            query = "SELECT * FROM Image WHERE md5 = \'{0}\'".format(md5)
            self.__cursor.execute(query)
            row = self.__cursor.fetchone()
            if row is not None:
                return Image(row)
            else:
                return None
        except MySQL.Error as err:
            print(err)
            return None
