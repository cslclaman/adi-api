from control.dbcontrol import Control
from model.aditag import AdiTag
from mysql.connector import Error

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
        except Error as err:
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
        except Error as err:
            print(err)
        self.disconnect()
        return adiTag

    def getByTagDictionary(self, dict):
        typ = dict['type']
        tag = dict['tag']
        return self.getByTypeAndTag(typ,tag)

    def getByTypeAndTag(self, type, tag):
        self.connect()
        adiTag = None
        try:
            query = "SELECT * FROM Adi_Tag WHERE type = \'{0}\' AND tag = \'{1}\'".format(type, tag)
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            if row is not None:
                adiTag = AdiTag(row)
        except Error as err:
            print(err)
        self.disconnect()
        return adiTag

    def create(self, adiTag):
        self.connect()
        new_aditag = None
        columns = "type,tag"
        values = "\'{0}\',\'{1}\'".format(adiTag.getType(),adiTag.getTag())
        query = "INSERT INTO Adi_Tag ({0}) VALUES ({1})".format(columns, values)
        try:
            self.cursor.execute(query)
            self.con.commit()
            new_aditag = self.getById(self.cursor.lastrowid)
        except Error as err:
            print(err)
        self.disconnect()
        return new_aditag
