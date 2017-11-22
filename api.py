# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, redirect, url_for
from control.dbimagecontrol import ImageControl
from control.dbimagesourcecontrol import ImageSourceControl
from control.dbtagcontrol import TagControl
from control.dbaditagcontrol import AdiTagControl
from model.tag import Tag
from model.image import Image
from model.imagesource import ImageSource
from model.aditag import AdiTag
import control.formats as formats

app = Flask(__name__, static_url_path='')
app.json_encoder = formats.JSONDateEncoder

ctrImage = ImageControl()
ctrImgSource = ImageSourceControl()
ctrTag = TagControl()
ctrAdiTag = AdiTagControl()

@app.route('/')
def index():
	return app.send_static_file("index.html")

@app.route('/image', methods=['GET'])
def image_list():
	jsonImageList = []

	page = request.args.get('page', 1, type=int)
	limit = request.args.get('limit', 25, type=int)
	tags = request.args.get('tags', "", type=str)
	source = request.args.get('source', "hide", type=str)
	rating = request.args.get('rating', "", type=str)

	for image in ctrImage.getList(tags,page,limit,rating):
		#the idea is to change Image serialize method to receive a list of sources to serialize
		#(if this code was Java, it's be an overloaded method, but... Python is python and overload is not too handful)
		#the list is to be created here
		if source == "show":
			#add all ImageSources related to this image in the list
			imageSource = ctrImgSource.getById(image.getPrimarySourceId())
			jsonImageList.append(image.serialize(imageSource))
		elif source == "primary":
			#add just primary source in list
			imageSource = ctrImgSource.getById(image.getPrimarySourceId())
			jsonImageList.append(image.serialize(imageSource))
		else:
			#well, the list here is empty.
			jsonImageList.append(image.serialize())
	return jsonify(jsonImageList), 200

@app.route('/image/<int:id>', methods=['GET'])
def image_view(id):
	source = request.args.get('source', "hide", type=str)
	image = ctrImage.getById(id)
	if image is None:
		return jsonify({}), 404
	else:
		#same as above
		if source == "show" or source == "primary":
			imgSource = ctrImgSource.getById(image.getPrimarySourceId())
			return jsonify(image.serialize(imgSource)), 200
		else:
			return jsonify(image.serialize()), 200

@app.route('/image/find', methods=['GET'])
def image_get():
	md5 = request.args.get('md5', "", type=str)
	id = request.args.get('id', -1, type=int)
	source = request.args.get('source', "hide", type=str)

	image = None
	if id != -1:
		image = ctrImage.getById(id)
	else:
		if md5 != "":
			image = ctrImage.getByMd5(md5)

	if image is None:
		return jsonify({}), 404
	else:
		return redirect(url_for("image_view",id = image.getId(), source = source))

@app.route('/image', methods=['POST'])
def image_create():
	json = request.get_json()
	newImage = Image(dict=json)
	newImage = ctrImage.create(newImage)
	if newImage is None:
		return jsonify({}), 404
	else:
		for tag in newImage.getTagList():
			adiTag = ctrAdiTag.getByTagDictionary(formats.parseAdiTag(tag))
			#print(tag + " => " + adiTag.)
			if adiTag is not None:
				ctrImage.addTag(newImage,adiTag)
		return jsonify(newImage.serialize()), 201

@app.route('/imagesource/<int:image_id>', methods=['GET'])
def imagesource_list(image_id):
	jsonImageSourceList = []
	name = request.args.get('name', "", type=str)
	for imageSource in ctrImgSource.getList(image_id,name):
		jsonImageSourceList.append(imageSource.serialize())
	return jsonify(jsonImageSourceList), 200

@app.route('/imagesource', methods=['POST'])
def imagesource_create():
	json = request.get_json()
	newImgSource = ImageSource(dict=json)
	newImgSource = ctrImgSource.create(newImgSource)
	if newImgSource is None:
		return jsonify({}), 404
	else:
		for tagName in newImgSource.getTagList():
			tag = ctrTag.getByTagName(tagName)
			if tag is not None:
				ctrImgSource.addTag(newImgSource,tag)
		return jsonify(newImgSource.serialize()), 201

@app.route('/tag', methods=['GET'])
def tag_list():
	jsonTagList = []

	page = request.args.get('page', 1, type=int)
	limit = request.args.get('limit', 50, type=int)
	name = request.args.get('name', "", type=str)
	searchType = request.args.get('search', "all", type=str)
	searchTag = request.args.get('association', "", type=str)
	showadi = request.args.get('adi_tag', "hide", type=str)

	adiTag = ctrAdiTag.getByTagDictionary(formats.parseAdiTag(searchTag))

	for tag in ctrTag.getList(page,limit,name,searchType,adiTag):
		if showadi == "show" and tag.hasAdiTag():
			adiTag = ctrAdiTag.getById(tag.getAdiTagId())
			jsonTagList.append(tag.serialize(adiTag))
		else:
			jsonTagList.append(tag.serialize())

	return jsonify(jsonTagList), 200

@app.route('/tag/<int:id>', methods=['GET'])
def tag_view(id):
	showadi = request.args.get('adi_tag', "hide", type=str)
	tag = ctrTag.getById(id)
	if tag is None:
		return jsonify({}), 404
	else:
		if showadi == "show" and tag.hasAdiTag():
			adiTag = ctrAdiTag.getById(tag.getAdiTagId())
			return jsonify(tag.serialize(adiTag)), 200
		else:
			return jsonify(tag.serialize()), 200

@app.route('/tag/<int:id>', methods=['PUT'])
def tag_edit(id):
	json = request.get_json()
	name = json['name']
	url = json['url']
	aditag = json['adi_tag']
	tag = ctrTag.getById(id)
	if tag is None:
		return jsonify({}), 404
	else:
		if name is not None:
			tag.setTag(name)
		if url is not None:
			tag.setUrl(url)
		if aditag is not None:
			tag.setAdiTagId(aditag)
		tag = ctrTag.update(tag)
		return jsonify(tag.serialize()), 200

@app.route('/tag/find', methods=['GET'])
def tag_get():
	id = request.args.get('id', -1, type=int)
	name = request.args.get('name', "", type=str)
	showadi = request.args.get('adi_tag', "hide", type=str)
	tag = None
	param = ""

	if id != -1:
		param = "id = {0}".format(id)
		tag = ctrTag.getById(id)
	else:
		if name != "":
			param = "name = {0}".format(name)
			tag = ctrTag.getByTagName(name)

	if tag is None:
		return jsonify({'error':"No tag found for the specified parameter",'parameter':param}), 404
	else:
		return redirect(url_for("tag_view",id = tag.getId(), adi_tag = showadi))

@app.route('/tag', methods=['POST'])
def tag_create():
	json = request.get_json()
	tag = json['name']
	url = json['url']
	newTag = Tag(tag=tag,url=url)
	newTag = ctrTag.create(newTag)
	if newTag is None:
		return jsonify({}), 404
	else:
		return jsonify(newTag.serialize()), 201

@app.route('/aditag', methods=['GET'])
def aditag_list():
	jsonAdiTagList = []
	page = request.args.get('page', 1, type=int)
	limit = request.args.get('limit', 50, type=int)
	type = request.args.get('type', "", type=str)
	name = request.args.get('name', "", type=str)
	for adiTag in ctrAdiTag.getList(page,limit,type,name):
		jsonAdiTagList.append(adiTag.serialize())
	return jsonify(jsonAdiTagList), 200

@app.route('/aditag/<int:id>', methods=['GET'])
def aditag_view(id):
	aditag = ctrAdiTag.getById(id)
	if aditag is None:
		return jsonify({}), 404
	else:
		return jsonify(aditag.serialize()), 200

@app.route('/aditag/find', methods=['GET'])
def aditag_get():
	id = request.args.get('id', -1, type=int)
	type = request.args.get('type', "", type=str)
	name = request.args.get('name', "", type=str)
	searchTag = request.args.get('tagstring', "", type=str)
	adiTag = None
	if id != -1:
		adiTag = ctrAdiTag.getById(id)
	else:
		if type != "" and name != "":
			adiTag = ctrAdiTag.getByTypeAndTag(type, name)
		else:
			if searchTag != "":
				adiTag = ctrAdiTag.getByTagDictionary(formats.parseAdiTag(searchTag))

	if adiTag is None:
		return jsonify({}), 404
	else:
		return redirect(url_for("aditag_view",id = adiTag.getId()))

@app.route('/aditag', methods=['POST'])
def aditag_create():
	json = request.get_json()
	type = json['type']
	name = json['name']
	tagList = json['tags']
	newAdiTag = AdiTag(type=type,tag=name)
	newAdiTag = ctrAdiTag.create(newAdiTag)
	if newAdiTag is None:
		return jsonify({}), 404
	else:
		if tagList is not None:
			for tagName in tagList:
				tag = ctrTag.getByTagName(tagName)
				if tag is not None:
					tag.setAdiTagId(newAdiTag.getId())
					tag = ctrTag.update(tag)
		return jsonify(newAdiTag.serialize()), 201

@app.route('/aditag/<int:id>', methods=['PUT'])
def aditag_edit(id):
	json = request.get_json()
	type = json['type']
	name = json['name']
	adiTag = ctrAdiTag.getById(id)
	if adiTag is None:
		return jsonify({}), 404
	else:
		if type is not None:
			adiTag.setType(type)
		if name is not None:
			adiTag.setTag(name)
		adiTag = ctrAdiTag.update(adiTag)
		return jsonify(adiTag.serialize()), 200

if __name__ == "__main__":
	app.run(debug=True, host="localhost")
