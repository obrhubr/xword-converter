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
	
	def import_puzzle(self, file, file_format):
		puzzle = None

		# Import puzzle in correct format
		if file_format == "json":
			puzzle = self.json.import_puzzle(file)
		elif file_format == "json_nyt":
			puzzle = self.json_nyt.import_puzzle(file)
		elif file_format == "puz":
			puzzle = self.puz.import_puzzle(file)
		else:
			raise Exception(f"Format '{file_format}' not supported.")
		
		return puzzle
	
	def export_puzzle(self, puzzle, file, file_format):
		# Export puzzle in correct format
		if file_format == "json":
			self.json.export_puzzle(puzzle, file)
		elif file_format == "json_nyt":
			self.json_nyt.export_puzzle(puzzle, file)
		elif file_format == "puz":
			self.puz.export_puzzle(puzzle, file)
		else:
			raise Exception(f"Format '{file_format}' not supported.")
	
	# Convert file
	def convert(self, input_file, input_format, output_file, output_format):
		puzzle = self.import_puzzle(input_file, input_format)
		self.export_puzzle(puzzle, output_file, output_format)
		return