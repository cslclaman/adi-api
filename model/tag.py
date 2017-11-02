class Tag:
    def __init__(self, row):
        self.__id = row[0]
        self.__tag = row[1]
        self.__url = row[2]
        self.__adiTag = row[3]

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
