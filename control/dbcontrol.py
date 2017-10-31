# -*- coding: utf-8 -*-
import dbconfig
from model.image import Image
from model.imagesource import ImageSource
from datetime import datetime
import mysql.connector as MySQL

MAX_LIMIT = 50

class ImageControl:
    def __init__(self):
        self.__con = MySQL.connect(user=dbconfig.user, password=dbconfig.password, host=dbconfig.host, database=dbconfig.database)
        self.__cursor = self.__con.cursor()

    def getList(self, tags, pagenum, limit, rating):
        listImages = []
        try:
            if (limit > MAX_LIMIT): limit = MAX_LIMIT
            if (limit < 1): limit = 1
            page = (pagenum - 1) * limit
            query = "SELECT * FROM Image WHERE tag_string LIKE \'{0}\' AND rating LIKE \'{1}\' LIMIT {2},{3}".format(("%"+tags+"%"),rating,page,limit)
            self.__cursor.execute(query)
            results = self.__cursor.fetchall()
            for row in results:
                image = Image(row)
                listImages.append(image)
        except MySQL.Error as err:
            print(err)
        return listImages;

    def getById(self, id):
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

    def getByMd5(self, md5):
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

    def create(self, image):
        id = image.getId()
        md5 = image.getMd5()
        file_path = image.getFilePath()
        tag_string = image.getTagString()
        rating = image.getRating()
        active = 1 if image.isActive() == True else 0
        file_size = image.getFileSize()
        creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        file_source = image.getFileSource()
        columns = "md5,file_path,tag_string,rating,active,file_size,creation_date,file_source"
        values = "\'{0}\',\'{1}\',\'{2}\',\'{3}\',{4},{5},\'{6}\',\'{7}\'".format(md5,file_path,tag_string,rating,active,file_size,creation_date,file_source)
        try:
            query = "INSERT INTO Image ({0}) VALUES ({1})".format(columns, values)
            self.__cursor.execute(query)
        except MySQL.Error as err:
            print(err)

class ImageSourceControl:
    def __init__(self):
        self.__con = MySQL.connect(user=USER, password=PASS, host=HOST, database=DB)
        self.__cursor = self.__con.cursor()

    def getList(self, image_id, name):
        listImageSources = []
        try:
            query = "SELECT * FROM Image_Source WHERE image = {0} and source_name like \'{1}\'".format(image_id, ("%"+name+"%"))
            self.__cursor.execute(query)
            results = self.__cursor.fetchall()
            for row in results:
                imagesrc = ImageSource(row)
                listImageSources.append(imagesrc)
        except MySQL.Error as err:
            print(err)
        return listImageSources;

    def getById(self, id):
        try:
            query = "SELECT * FROM Image_Source WHERE id = {0}".format(id)
            self.__cursor.execute(query)
            row = self.__cursor.fetchone()
            if row is not None:
                return ImageSource(row)
            else:
                return None
        except MySQL.Error as err:
            print(err)
            return None
