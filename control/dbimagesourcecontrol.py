from control.dbcontrol import Control
from model.imagesource import ImageSource

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
