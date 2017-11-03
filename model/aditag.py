class AdiTag:
    def __init__(self, row):
        self.__id = row[0]
        self.__type = row[1]
        self.__tag = row[2]

    def getId(self):
        return self.__id
    def setId(self,id):
        self.__id = id

    def getType(self):
        return self.__type
    def setType(self, type):
        self.__type = type

    def getTag(self):
        return self.__tag
    def setTag(self):
        self.__tag = tag

    def serialize(self):
        json = {
            "id": self.__id,
            "type": self.__type,
            "tag": self.__tag
        }
        return json

    def __str__(self):
        return "({1}){2}".format(self.__type,self.__tag)
