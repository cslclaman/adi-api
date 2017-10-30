# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from model.image import Image
from control.dbcontrol import ImageControl

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
	return app.send_static_file("index.html")

@app.route('/image/list', methods=['GET'])
def image_list():
	ctr = ImageControl()
	jsonImageList = []
	page = request.args.get('page', 1, type=int)
	limit = request.args.get('limit', 25, type=int)
	tags = request.args.get('tags', "", type=str)
	for image in ctr.get_image_list(tags,page,limit):
		jsonImageList.append(image.serialize())
	return jsonify(jsonImageList), 200

@app.route('/image/<int:id>', methods=['GET'])
def image_by_id(id):
	ctr = ImageControl()
	image = ctr.get_image_by_id(id)
	if image is None:
		return jsonify({})
	else:
		return jsonify(image.serialize()), 200

if __name__ == "__main__":
	app.run(debug=True, host="localhost")
