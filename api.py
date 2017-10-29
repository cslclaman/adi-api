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
	tags = request.args.get('tags', "", type=str)
	for image in ctr.get_image_list(page,tags):
		jsonImageList.append(image.serialize())
	return jsonify(jsonImageList), 200

if __name__ == "__main__":
	app.run(debug=True, host="localhost")
