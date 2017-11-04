# -*- coding: utf-8 -*-
import control.dbconfig as dbconfig
from model.image import Image
from model.imagesource import ImageSource
from model.tag import Tag
from model.aditag import AdiTag
from datetime import datetime
import mysql.connector as MySQL

class Control:
    def __init__(self):
        self.con = None
        self.cursor = None

    def connect(self):
        self.con = MySQL.connect(user=dbconfig.user, password=dbconfig.password, host=dbconfig.host, database=dbconfig.database)
        self.cursor = self.con.cursor()

    def disconnect(self):
        self.cursor.close
        self.con.close()

class ImageControl(Control):
    def __init__(self):
        Control.__init__(self)
        self.__maxLimit = 50

    def getList(self, tags, pagenum, limit, rating):
        self.connect()
        listImages = []
        try:
            if (limit > self.__maxLimit): limit = self.__maxLimit
            if (limit < 1): limit = 1
            page = (pagenum - 1) * limit
            query = "SELECT * FROM Image WHERE tag_string LIKE \'{0}\' AND rating LIKE \'{1}\' LIMIT {2},{3}".format(("%"+tags+"%"),("%"+rating+"%"),page,limit)
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            for row in results:
                image = Image(row)
                listImages.append(image)
        except MySQL.Error as err:
            print(err)
        self.disconnect()
        return listImages;

    def getById(self, id):
        self.connect()
        image = None
        try:
            query = "SELECT * FROM Image WHERE id = {0}".format(id)
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row is not None:
                image = Image(row)
        except MySQL.Error as err:
            print(err)
        self.disconnect()
        return image

    def getByMd5(self, md5):
        self.connect()
        image = None
        try:
            query = "SELECT * FROM Image WHERE md5 = \'{0}\'".format(md5)
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row is not None:
                image = Image(row)
        except MySQL.Error as err:
            print(err)
        self.disconnect()
        return image

    def create(self, image):
        self.connect()
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
            self.cursor.execute(query)
            self.con.commit()
        except MySQL.Error as err:
            print(err)
        self.disconnect()

class ImageSourceControl(Control):
    def __init__(self):
        Control.__init__(self)

    def getList(self, image_id, name):
        self.connect()
        listImageSources = []
        try:
            query = "SELECT * FROM Image_Source WHERE image = {0} and source_name like \'{1}\'".format(image_id, ("%"+name+"%"))
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            for row in results:
                imagesrc = ImageSource(row)
                listImageSources.append(imagesrc)
        except MySQL.Error as err:
            print(err)
        self.disconnect()
        return listImageSources;

    def getById(self, id):
        self.connect()
        imageSource = None
        try:
            query = "SELECT * FROM Image_Source WHERE id = {0}".format(id)
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row is not None:
                imageSource =  ImageSource(row)
        except MySQL.Error as err:
            print(err)
        self.disconnect()
        return imageSource

class TagControl(Control):
    def __init__(self):
        Control.__init__(self)
        self.__maxLimit = 100

    def getList(self, pagenum, limit, name, search, adi_tag = None):
        self.connect()
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
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            for row in results:
                tag = Tag(row=row)
                listTags.append(tag)
        except MySQL.Error as err:
            print(err)
        self.disconnect()
        return listTags;

    def getById(self, id):
        self.connect()
        tag = None
        try:
            query = "SELECT * FROM Tag WHERE id = {0}".format(id)
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row is not None:
                tag = Tag(row=row)
        except MySQL.Error as err:
            print(err)
        self.disconnect()
        return tag

    def getByTagName(self, name):
        self.connect()
        tag = None
        try:
            query = "SELECT * FROM Tag WHERE tag = \'{0}\'".format(name)
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row is not None:
                tag = Tag(row=row)
        except MySQL.Error as err:
            print(err)
        self.disconnect()
        return tag

    def create(self, tag):
        self.connect()
        new_tag = None
        columns = "tag,url"
        values = "\'{0}\',\'{1}\'".format(tag.getTag(),tag.getUrl())
        query = "INSERT INTO Tag ({0}) VALUES ({1})".format(columns, values)
        try:
            self.cursor.execute(query)
            self.con.commit()
            new_tag = self.getById(self.cursor.lastrowid)
        except MySQL.Error as err:
            print(err)
        self.disconnect()
        return new_tag

class AdiTagControl(Control):
    def __init__(self):
        Control.__init__(self)
        self.__maxLimit = 100

    def getList(self, pagenum, limit, tag_type, tag_tag):
        self.connect()
        listAdiTags = []
        try:
            if (limit > self.__maxLimit): limit = self.__maxLimit
            if (limit < 1): limit = 1
            page = (pagenum - 1) * limit
            query = "SELECT * FROM Adi_Tag WHERE type LIKE \'{0}\' and tag LIKE \'{1}\' ORDER BY id LIMIT {2},{3}".format("%"+tag_type+"%","%"+tag_tag+"%",page,limit)
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            for row in results:
                aditag = AdiTag(row)
                listAdiTags.append(aditag)
        except MySQL.Error as err:
            print(err)
        self.disconnect()
        return listAdiTags;

    def getById(self, id):
        self.connect()
        adiTag = None
        try:
            query = "SELECT * FROM Adi_Tag WHERE id = {0}".format(id)
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row is not None:
                adiTag = AdiTag(row)
        except MySQL.Error as err:
            print(err)
        self.disconnect()
        return adiTag

    def getByTagDictionary(self, dict):
        typ = dict['type']
        tag = dict['tag']
        return self.getByTypeAndTag(typ,tag)

    def getByTypeAndTag(self, tag_type, tag_tag):
        self.connect()
        adiTag = None
        try:
            query = "SELECT * FROM Adi_Tag WHERE type = \'{0}\' AND tag = \'{1}\'".format(tag_type, tag_tag)
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row is not None:
                adiTag = AdiTag(row)
        except MySQL.Error as err:
            print(err)
        self.disconnect()
        return adiTag
