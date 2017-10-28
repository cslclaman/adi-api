class Image:

	def __init__(self, row):
		self.__id = row[0]
		self.__md5 = row[1]
		self.__filePath = row[2]
		self.__tagString = row[3]
		self.__rating = row[4]
		self.__active = True if row[5] == 1 else False
		self.__fileSize = row[6]
		self.__fileSource = row[7]
		self.__creationDate = row[8]
		self.__lastUpdate = row[9]
		#self.__primarySource = row[10]
		self.__sourceName = row[11]

	def getId(self):
		return self.__id
	def setId(self,id):
		self.__id = id

	def getMd5(self):
		return self.__md5
	def setMd5(self,md5):
		self.__md5 = md5

	def getFilePath(self):
		return self.__filePath
	def setFilePath(self,filePath):
		self.__filePath = filePath

	def getTagString(self):
		return self.__tagString
	def setTagString(self,tagString):
		self.__tagString = tagString

	def getRating(self):
		return self.__rating
	def setRating(self,rating):
		self.__rating = rating

	def isActive(self):
		return self.__active
	def setActive(self,active):
		self.__active = active

	def getFileSize(self):
		return self.__fileSize
	def setFileSize(self,fileSize):
		self.__fileSize = fileSize

	def getFileSource(self):
		return self.__fileSource
	def setFileSource(self,fileSource):
		self.__fileSource = fileSource

	def getCreationDate(self):
		return self.__creationDate
	def setCreationDate(self,creationDate):
		self.__creationDate = creationDate

	def getLastUpdate(self):
		return self.__lastUpdate
	def setLastUpdate(self,lastUpdate):
		self.__lastUpdate = lastUpdate

	def getSourceName(self):
		return self.__sourceName
	def setSourceName(self,sourceName):
		self.__sourceName = sourceName

	def __str__(self):
		return "{0} - {1} - {2}".format(self.__id, self.__md5, self.__filePath)
