# -*- coding: utf-8 -*-
import control.dbconfig as dbconfig
from model.image import Image
from model.imagesource import ImageSource
from model.tag import Tag
from model.aditag import AdiTag
from datetime import datetime
import mysql.connector as MySQL

class ImageControl:
    def __init__(self):
        self.__con = MySQL.connect(user=dbconfig.user, password=dbconfig.password, host=dbconfig.host, database=dbconfig.database)
        self.__cursor = self.__con.cursor()
        self.__maxLimit = 50

    def getList(self, tags, pagenum, limit, rating):
        listImages = []
        try:
            if (limit > self.__maxLimit): limit = self.__maxLimit
            if (limit < 1): limit = 1
            page = (pagenum - 1) * limit

            query = "SELECT * FROM Image WHERE tag_string LIKE \'{0}\' AND rating LIKE \'{1}\' LIMIT {2},{3}".format(("%"+tags+"%"),("%"+rating+"%"),page,limit)
            self.__cursor.execute(query)
            results = self.__cursor.fetchall()
            for row in results:
                image = Image(row)
                listImages.append(image)
        except MySQL.Error as err:
            print(err)
        return listImages;

    def getById(self, id):
        image = None
        try:
            query = "SELECT * FROM Image WHERE id = {0}".format(id)
            self.__cursor.execute(query)
            row = self.__cursor.fetchone()
            if row is not None:
                image = Image(row)
        except MySQL.Error as err:
            print(err)
        return image

    def getByMd5(self, md5):
        image = None
        try:
            query = "SELECT * FROM Image WHERE md5 = \'{0}\'".format(md5)
            self.__cursor.execute(query)
            row = self.__cursor.fetchone()
            if row is not None:
                image = Image(row)
        except MySQL.Error as err:
            print(err)
        return image

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
        self.__con = MySQL.connect(user=dbconfig.user, password=dbconfig.password, host=dbconfig.host, database=dbconfig.database)
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
        imageSource = None
        try:
            query = "SELECT * FROM Image_Source WHERE id = {0}".format(id)
            self.__cursor.execute(query)
            row = self.__cursor.fetchone()
            if row is not None:
                imageSource =  ImageSource(row)
        except MySQL.Error as err:
            print(err)
        return imageSource

class TagControl:
    def __init__(self):
        self.__con = MySQL.connect(user=dbconfig.user, password=dbconfig.password, host=dbconfig.host, database=dbconfig.database)
        self.__cursor = self.__con.cursor()
        self.__maxLimit = 100

    def getList(self, pagenum, limit, name, search, adi_tag = None):
        listTags = []
        try:
            if (limit > self.__maxLimit): limit = self.__maxLimit
            if (limit < 1): limit = 1
            page = (pagenum - 1) * limit
            query_a = ""
            if adi_tag is not None and adi_tag.getId() is not None:
                query_a = "AND adi_tag = {0}".format(adi_tag.getId())

            query_b = ""
            if search == "unassociated":
                query_b = "AND adi_tag IS NULL"
            elif search == "associated":
                query_b = "AND adi_tag IS NOT NULL"

            query = "SELECT * FROM Tag WHERE tag LIKE \'{0}\' {1} {2} LIMIT {3},{4}".format("%"+name+"%",query_a,query_b,page,limit)
            self.__cursor.execute(query)
            results = self.__cursor.fetchall()
            for row in results:
                tag = Tag(row=row)
                listTags.append(tag)
        except MySQL.Error as err:
            print(err)
        return listTags;

    def getById(self, id):
        tag = None
        try:
            query = "SELECT * FROM Tag WHERE id = {0}".format(id)
            self.__cursor.execute(query)
            row = self.__cursor.fetchone()
            if row is not None:
                tag = Tag(row=row)
        except MySQL.Error as err:
            print(err)
        return tag

    def getByTagName(self, name):
        tag = None
        try:
            query = "SELECT * FROM Tag WHERE tag = \'{0}\'".format(name)
            self.__cursor.execute(query)
            row = self.__cursor.fetchone()
            if row is not None:
                tag = Tag(row=row)
        except MySQL.Error as err:
            print(err)
        return tag

    def create(self, tag):
        new_tag = None
        columns = "tag,url"
        values = "\'{0}\',\'{1}\'".format(tag.getTag(),tag.getUrl())
        query = "INSERT INTO Tag ({0}) VALUES ({1})".format(columns, values)
        print(query)
        try:
            self.__cursor.execute(query)
            new_tag = self.getById(self.__cursor.lastrowid)
        except MySQL.Error as err:
            print(err)
        return new_tag

class AdiTagControl:
    def __init__(self):
        self.__con = MySQL.connect(user=dbconfig.user, password=dbconfig.password, host=dbconfig.host, database=dbconfig.database)
        self.__cursor = self.__con.cursor()
        self.__maxLimit = 100

    def getList(self, pagenum, limit, tag_type, tag_tag):
        listAdiTags = []
        try:
            if (limit > self.__maxLimit): limit = self.__maxLimit
            if (limit < 1): limit = 1
            page = (pagenum - 1) * limit
            query = "SELECT * FROM Adi_Tag WHERE type LIKE \'{0}\' and tag LIKE \'{1}\' ORDER BY id LIMIT {2},{3}".format("%"+tag_type+"%","%"+tag_tag+"%",page,limit)
            self.__cursor.execute(query)
            results = self.__cursor.fetchall()
            for row in results:
                aditag = AdiTag(row)
                listAdiTags.append(aditag)
        except MySQL.Error as err:
            print(err)
        return listAdiTags;

    def getById(self, id):
        adiTag = None
        try:
            query = "SELECT * FROM Adi_Tag WHERE id = {0}".format(id)
            self.__cursor.execute(query)
            row = self.__cursor.fetchone()
            if row is not None:
                adiTag = AdiTag(row)
        except MySQL.Error as err:
            print(err)
        return adiTag

    def getByTagDictionary(self, dict):
        typ = dict['type']
        tag = dict['tag']
        return self.getByTypeAndTag(typ,tag)

    def getByTypeAndTag(self, tag_type, tag_tag):
        adiTag = None
        try:
            query = "SELECT * FROM Adi_Tag WHERE type = \'{0}\' AND tag = \'{1}\'".format(tag_type, tag_tag)
            self.__cursor.execute(query)
            row = self.__cursor.fetchone()
            if row is not None:
                adiTag = AdiTag(row)
        except MySQL.Error as err:
            print(err)
        return adiTag
