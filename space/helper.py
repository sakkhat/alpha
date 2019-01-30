
from django.core.files.storage import FileSystemStorage as FSS


from PIL import Image
from io import BytesIO
from time import time
from os import makedirs, remove
from os.path import isdir


class ImageHandler():

	def save(loc, bytes_date, quality=90, max_width=1000):
		folder = FSS(location = loc)
		
		img, exct = ImageHandler.__resize(bytes_date)

		file_name = str(int(time()*1000000))+'.'+exct

		if not isdir(f.location):
			makedirs(f.location)

		file_path = f.location+'/'+file_name

		img.save(file_path, format=exct, quality=quality)

		return file_path



	def delete(location):
		try:
			remove(location)
			return True
		except FileNotFoundError as e:
			return False



	def __resize(bytes_date, max_width=1000):
		"""
		resize the image and return the bytes data
		and image format
		"""
		img = Image.open(BytesIO(bytes_date))
		size = img.size
		#image max_width
		if size[1] > max_width:
			req_height = int(float(1000*size[1])/size[0])
			return img.resize((max_width, req_height)), img.format