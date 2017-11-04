from control.dbcontrol import Control
from model.image import Image
from datetime import datetime

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
