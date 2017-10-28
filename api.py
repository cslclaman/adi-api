# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
import MySQLdb
from model.image import Image

app = Flask(__name__)
images = []
con = MySQLdb.connect(host="localhost",user="appuser",passwd="ms987654",database="adi6_db")

cursor = con.cursor()

@app.route('/')
def index():
	return """<h1>API</h1>
	"""

@app.route('/image/list', methods=['GET'])
def image_list():
	cursor.execute("Select * from image limit 100")
	results = cursor.fetchall()
	print("{0} {1:10} {2} {3}".format('ID', 'MD5', 'PATH'))

	for row in results:
		print(row)
		#produtos.append(model.produto(row))
	return jsonify(results), 200

if __name__ == "__main__":
	app.run(debug=True, host="localhost")
