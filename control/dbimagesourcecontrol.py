from control.dbcontrol import Control
from model.imagesource import ImageSource
from mysql.connector import Error

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
                imagesrc = ImageSource(row=row)
                listImageSources.append(imagesrc)
        except Error as err:
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
                imageSource =  ImageSource(row=row)
        except Error as err:
            print(err)
        self.disconnect()
        return imageSource

    def create(self, imageSource):
        self.connect()
        newsource = None
        image = imageSource.getImageId()
        sourceName = imageSource.getSourceName()
        sourceId = imageSource.getSourceId()
        sourceOffline = 1 if imageSource.isSourceOffline() else 0
        imageDeleted = 1 if imageSource.isImageDeleted() else 0
        imageCensored = 1 if imageSource.isImageCensored() else 0
        imageBanned = 1 if imageSource.isImageBanned() else 0
        columns = "image,source_name,source_id,source_offline,image_deleted,image_censored,image_banned"
        values = "{0},\'{1}\',\'{2}\',{3},{4},{5},{6}".format(image,sourceName,sourceId,sourceOffline,imageDeleted,imageCensored,imageBanned)
        if imageSource.getPostUrl() is not None:
            columns += ",post_url"
            values += ",\'{0}\'".format(imageSource.getPostUrl())
        if imageSource.getFileUrl() is not None:
            columns += ",file_url"
            values += ",\'{0}\'".format(imageSource.getFileUrl())
        if imageSource.getUploadDate() is not None:
            columns += ",upload_date"
            values += ",\'{0}\'".format(imageSource.getUploadDate().strftime('%Y-%m-%d %H:%M:%S'))
        if imageSource.getMd5() is not None:
            columns += ",md5"
            values += ",\'{0}\'".format(imageSource.getMd5())
        if imageSource.getFileSize() is not None:
            columns += ",file_size"
            values += ",{0}".format(imageSource.getFileSize())
        if imageSource.getTagString() is not None:
            columns += ",tag_string"
            values += ",\'{0}\'".format(imageSource.getTagString())
        if imageSource.getRating() is not None:
            columns += ",rating"
            values += ",\'{0}\'".format(imageSource.getRating())
        try:
            query = "INSERT INTO Image ({0}) VALUES ({1})".format(columns, values)
            self.cursor.execute(query)
            self.con.commit()
            newsource = self.getById(self.cursor.lastrowid)
        except Error as err:
            print(err)
        self.disconnect()
        return newsource

    def addTag(self, source, tag):
        self.connect()
        assoc = False
        try:
            query = "INSERT INTO Source_Tags (image_source, tag) VALUES ({0}, {1})".format(source.getId(), tag.getId())
            self.cursor.execute(query)
            self.con.commit()
            assoc = True
        except Error as err:
            print(err)
        self.disconnect()
        return assoc
