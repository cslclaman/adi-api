# -*- coding: utf-8 -*-
from model.image import Image
from control.dbcontrol import ImageControl

def create_image():
	img = Image(111,"505050","c:\\aaa")
	return img

def get_images():
	ctr = ImageControl()
	for image in ctr.get_image_list():
		print(image)

get_images()
