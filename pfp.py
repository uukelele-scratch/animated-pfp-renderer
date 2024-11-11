import scratchattach as sa
import requests
from PIL import Image, ImageSequence
from io import BytesIO
import numpy as np

session = sa.login("username", "password")
cloud = session.connect_cloud("1094442040")
client = cloud.requests(respond_order="finish",no_packet_loss=True)

@client.event
def on_ready():
	print("[pfp renderer] started")

@client.request
def ping():
	return "pong"

def rgb2scratch(rgb):
	r, g, b = rgb
	return r * 256**2 + g * 256 + b

def process_frame(image):
	resized_img = image.resize((16, 16))
	image_data = []
	for y in range(16):
		row = []
		for x in range(16):
			rgb = resized_img.getpixel((x, y))[:3]
			row.append(rgb2scratch(rgb))
		image_data.append(row)
	return image_data


@client.request
def gifornot(user, client):
	user_obj = sa.get_user(user)
	icon = requests.get(user_obj.icon_url)
	img = Image.open(BytesIO(icon.content))
	if img.format == 'GIF':
		return "gif"
	else:
		return "not"

@client.request
def grab_image(user, client):
	user_obj = sa.get_user(user)
	icon = requests.get(user_obj.icon_url)
	img = Image.open(BytesIO(icon.content))
	if img.format != 'GIF':
		size = 64
		resized_img = img.resize((size, size))
		image_data = []
		for y in range(size):
			row = []
			for x in range(size):
				rgb = resized_img.getpixel((x, y))[:3]
				row.append(rgb2scratch(rgb))
			image_data.append(row)
		return image_data
	else:
		frames_data = []
		for frame in ImageSequence.Iterator(img):
			frame = frame.convert('RGB')
			frame_data = process_frame(frame)
			frames_data.append(frame_data)
		return frames_data

client.start()