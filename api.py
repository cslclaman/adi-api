# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from model.image import Image
from control.dbcontrol import ImageControl, ImageSourceControl

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
	return app.send_static_file("index.html")

@app.route('/image/list', methods=['GET'])
def image_list():
	ctrImage = ImageControl()
	ctrImgSource = ImageSourceControl()
	jsonImageList = []
	page = request.args.get('page', 1, type=int)
	limit = request.args.get('limit', 25, type=int)
	tags = request.args.get('tags', "", type=str)
	source = request.args.get('source', False, type=bool)
	rating = request.args.get('rating', "", type=str)
	for image in ctrImage.getList(tags,page,limit,rating):
		if source:
			imgSource = ctrImgSource.getById(image.getPrimarySourceId())
			jsonImageList.append(image.serialize(imgSource))
		else:
			jsonImageList.append(image.serialize())
	return jsonify(jsonImageList), 200

@app.route('/image/<int:id>', methods=['GET'])
def image_by_id(id):
	ctrImage = ImageControl()
	ctrImgSource = ImageSourceControl()
	source = request.args.get('source', False, type=bool)
	image = ctrImage.getById(id)
	if image is None:
		return jsonify({}), 400
	else:
		if source:
			imgSource = ctrImgSource.getById(image.getPrimarySourceId())
			return jsonify(image.serialize(imgSource)), 200
		else:
			return jsonify(image.serialize()), 200

@app.route('/imagesource/<int:image_id>', methods=['GET'])
def image_source_by_image_id(image_id):
	ctrImgSource = ImageSourceControl()
	jsonImageSourceList = []
	name = request.args.get('name', "", type=str)
	for imageSource in ctrImgSource.getList(image_id,name):
		jsonImageSourceList.append(imageSource.serialize())
	return jsonify(jsonImageSourceList), 200

if __name__ == "__main__":
	app.run(debug=True, host="localhost")
