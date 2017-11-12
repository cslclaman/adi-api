# -*- coding: utf-8 -*-
from datetime import datetime

class ImageSource:
	def __init__(self, row=None, dict=None):
		if row is not None:
			self.__id = row[0]
			self.__image = row[1]
			self.__sourceName = row[2]
			self.__sourceId = row[3]
			self.__postUrl = row[4]
			self.__fileUrl = row[5]
			self.__uploadDate = row[6]
			self.__md5 = row[7]
			self.__fileSize = row[8]
			self.__tagString = row[9]
			self.__sourceOffline = True if row[10] == 1 else False
			self.__imageDeleted = True if row[11] == 1 else False
			self.__imageCensored = True if row[12] == 1 else False
			self.__imageBanned = True if row[13] == 1 else False
			self.__rating = row[14]
		else:
			self.__id = 0
			if dict is not None:
				self.__image = dict['image_id']
				self.__sourceName = dict['source_name']
				self.__sourceId = dict['source_id']
				self.__postUrl = dict['post_url']
				self.__fileUrl = dict['file_url']
				if dict['upload_date'] is None:
					self.__uploadDate = None
				else:
					self.__uploadDate = datetime.strptime(dict['upload_date'], '%Y-%m-%d %H:%M:%S')
				self.__md5 = dict['md5']
				self.__fileSize = dict['file_size']
				self.__tagString = dict['tag_string']
				self.__sourceOffline = dict['source_offline']
				self.__imageDeleted = dict['image_deleted']
				self.__imageCensored = dict['image_censored']
				self.__imageBanned = dict['image_banned']
				self.__rating = dict['rating']

	def getId(self):
		return self.__id
	def setId(self,id):
		self.__id = id

	def getImage(self):
		return self.__image
	def setImage(self,image):
		self.__image = image

	def getSourceName(self):
		return self.__sourceName
	def setSourceName(self, sourceName):
		self.__sourceName = sourceName

	def getSourceId(self):
		return self.__sourceId
	def setSourceId(self, sourceId):
		self.__sourceId = sourceId

	def getPostUrl(self):
		return self.__postUrl
	def setPostUrl(self, postUrl):
		self.__postUrl = postUrl

	def getFileUrl(self):
		return self.__fileUrl
	def setFileUrl(self, fileUrl):
		self.__fileUrl = fileUrl

	def getUploadDate(self):
		return self.__uploadDate
	def setUploadDate(self, uploadDate):
		self.__uploadDate = uploadDate

	def getMd5(self):
		return self.__md5
	def setMd5(self,md5):
		self.__md5 = md5

	def getFileSize(self):
		return self.__fileSize
	def setFileSize(self,fileSize):
		self.__fileSize = fileSize

	def getTagString(self):
		return self.__tagString
	def setTagString(self,tagString):
		self.__tagString = tagString

	def isSourceOffline(self):
		return self.__sourceOffline
	def setSourceOffline(self,sourceOffline):
		self.__sourceOffline = sourceOffline

	def isImageDeleted(self):
		return self.__imageDeleted
	def setImageDeleted(self,imageDeleted):
		self.__imageDeleted = imageDeleted

	def isImageCensored(self):
		return self.__imageCensored
	def setImageCensored(self,imageCensored):
		self.__imageCensored = imageCensored

	def isImageBanned(self):
		return self.__imageBanned
	def setImageBanned(self,imageBanned):
		self.__imageBanned = imageBanned

	def getRating(self):
		return self.__rating
	def setRating(self,rating):
		self.__rating = rating

	def serialize(self):
		return {
			"id": self.__id,
			"source_name": self.__sourceName,
			"source_id": self.__sourceId,
			"post_url": self.__postUrl,
			"file_url": self.__fileUrl,
			"upload_date": self.__uploadDate,
			"md5": self.__md5,
			"file_size": self.__fileSize,
			"tag_string": self.__tagString,
			"source_offline": self.__sourceOffline,
			"image_deleted": self.__imageDeleted,
			"image_censored": self.__imageCensored,
			"image_banned": self.__imageBanned,
			"rating": self.__rating
		}

	def __str__(self):
		return "{0} {1} - {2}".format(self.__sourceName, self.__sourceId, self.__md5)
