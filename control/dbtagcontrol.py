from control.dbcontrol import Control
from model.tag import Tag
from mysql.connector import Error

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
        except Error as err:
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
        except Error as err:
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
        except Error as err:
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
        except Error as err:
            print(err)
        self.disconnect()
        return new_tag

    def update(self, tag):
        id = tag.getId()
        upd = self.getById(id)

        params = ""
        if tag.getTag() != upd.getTag():
            params = params + "tag = \'{0}\'".format(tag.getTag())
        if tag.getUrl() != upd.getUrl():
            if params:
                params = params + ","
            params = params + "url = \'{0}\'".format(tag.getUrl())
        if tag.getAdiTagId() != upd.getAdiTagId():
            if params:
                params = params + ","
            params = params + "adi_tag = {0}".format(tag.getAdiTagId())

        self.connect()
        query = "UPDATE Tag SET {1} WHERE id = {0}".format(id,params)
        try:
            self.cursor.execute(query)
            self.con.commit()
            upd = self.getById(id)
        except Error as err:
            print(err)
        self.disconnect()
        return upd
