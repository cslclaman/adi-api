class Tag:
    def __init__(self, row=None, id=0, tag="", url=""):
        if row is not None:
            self.__id = row[0]
            self.__tag = row[1]
            self.__url = row[2]
            self.__adiTag = row[3]
        else:
            self.__id = id
            self.__tag = tag
            if url:
                self.__url = url
            else:
                self.__url = tag
            self.__adiTag = None

    def getId(self):
        return self.__id
    def setId(self, id):
        self.__id = id

    def getTag(self):
        return self.__tag
    def setTag(self, tag):
        self.__tag = tag

    def getUrl(self):
        return self.__url
    def setUrl(self, url):
        self.__url = url

    def getAdiTagId(self):
        return self.__adiTag
    def setAdiTagId(self, adiTag):
        self.__adiTag = adiTag

    def hasAdiTag(self):
        return self.__adiTag is not None

    def serialize(self, adiTag=None):
        json = {
            "id": self.__id,
            "tag": self.__tag,
            "url": self.__url
        }
        if adiTag is not None:
            json["adi_tag"] = adiTag.serialize()
        return json

    def __str__(self):
        return self.__tag
