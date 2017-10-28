# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from model.image import Image
from control.dbcontrol import ImageControl

app = Flask(__name__)

@app.route('/')
def index():
	return """<h1>API</h1>
	<ul>
	<li><b>/image/list</b> = List all images (limited to 25 in each request)
		<ul>
			<li><i>page</i> (optional) = page number</li>
			<li><i>tags</i> (optional) = select only images that contains the specified tags</li>
		</ul>
	</li>
	"""

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
