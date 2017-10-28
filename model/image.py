class Image:
	def __init__(self, id=0, md5="", filePath=""):
		self.__id = id
		self.__md5 = md5
		self.__filePath = filePath

	#def __init__(self, dbline):
	#	self.__id = dbline[0]
	#	self.__md5 = dbline[1]

	def getId():
		return __id
	def setId(self,id):
		self.__id = id

	def getMd5():
		return __md5
	def setMd5(self,md5):
		self.__md5 = md5

	def getFilePath():
		return __filePath
	def setFilePath(self,filePath):
		self.__filePath = filePath

	def getTagString():
		return __tagString
	def setTagString(self,tagString):
		self.__tagString = tagString

	def getRating():
		return __rating
	def setRating(self,rating):
		self.__rating = rating

	def isActive():
		return __active
	def setActive(self,active):
		self.__active = active

	def getFileSize():
		return __fileSize
	def setFileSize(self,fileSize):
		self.__fileSize = fileSize

	def getFileSource():
		return __fileSource
	def setFileSource(self,fileSource):
		self.__fileSource = fileSource

	def getCreationDate():
		return __creationDate
	def setCreationDate(self,creationDate):
		self.__creationDate = creationDate

	def getLastUpdate():
		return __lastUpdate
	def setLastUpdate(self,lastUpdate):
		self.__lastUpdate = lastUpdate

	def getSourceName():
		return __sourceName
	def setSourceName(self,sourceName):
		self.__sourceName = sourceName

	def __str__(self):
		return "{0} - {1} - {2}".format(self.__id, self.__md5, self.__filePath)
