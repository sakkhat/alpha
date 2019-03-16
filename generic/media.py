from django.core.files.storage import FileSystemStorage as FSS

from generic.variables import now_md5_hashed, FILE_CHUNK_SIZE

from io import BytesIO
from PIL import Image as _Image
from time import time
from os import remove, makedirs
from os.path import isdir


class Image():

	THUMBNAIL_SIZE = (50,50)

	def load(file_stream=None, path=None, raw=None):
		img_file = None
		if file_stream is not None:
			if file_stream.multiple_chunks(FILE_CHUNK_SIZE):
				file_stream.chunks(FILE_CHUNK_SIZE)
			bytes_data = file_stream.read()
			img_file = _Image.open(BytesIO(bytes_data))

		elif path is not None:
			img_file = _Image.open(path)

		elif raw is not None:
			img_file = _Image.open(BytesIO(raw))

		return img_file


	def save(loc, file):
		storage = FSS(location = loc)
		filename = now_md5_hashed(8)+'.'+file.format

		if isdir(storage.location) == False:
			makedirs(storage.location)

		file.save(storage.location+'/'+filename, format=file.format, quality=90)

		return '/'+loc+'/'+filename


	def delete(loc):
		try:
			remove(loc)
			return True
		except Exception as e:
			try:
				remove(loc[1:])
				return True
			except Exception as e:
				pass
			return False


	def resize(file, new_width=None, new_height=None, new_size=None):
		"""
		Doc here

		"""
		# size is a tuple: (width, height)
		size = file.size
		extension = file.format
		new_file = None

		if new_width is not None:
			relate_height = int(float(new_width*size[1])/size[0])
			new_file = file.resize((new_width,relate_height))

		elif new_height is not None:
			relate_width = int(float(new_height*size[0])/size[1])
			new_file = file.resize((relate_width, new_height))

		elif new_size is not None:
			new_file = file.resize(new_size)


		else:
			if size[1] > 1000: 
				height = int(float(1000*size[1])/size[0])
				new_file = file.resize((1000,height))

		if new_file is not None:
			new_file.format = extension
			return new_file

		return file


	def is_valid_format(filename):

		filename = filename.lower()
		dotindex = filename.rfind('.')
		if dotindex != -1:
			extension = filename[dotindex:len(filename)]
			if extension == '.jpg':
				return True
			elif extension == '.png':
				return True
			elif extension == '.jpeg':
				return True
		
		return False	
