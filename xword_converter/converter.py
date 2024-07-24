from .plugins.json import Plugin as json_converter
from .plugins.json_nyt import Plugin as json_nyt_converter
from .plugins.puz import Plugin as puz_converter

class Converter:
	def __init__(self):
		self.formats = ["json_nyt", "json", "puz"]

		self.json = json_converter()
		self.json_nyt = json_nyt_converter()
		self.puz = puz_converter()

		return