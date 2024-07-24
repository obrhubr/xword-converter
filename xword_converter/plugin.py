class Plugin:
	def __init__(self):
		return
	
	# Parsing and serializing as handled differently for each file type
	def parse(self, puzzle_text):
		raise Exception("Not implemented.")
	
	def serialize(self, puzzle):
		raise Exception("Not implemented.")
	
	# Writing and reading, by default as normal text
	# But can be overriden by plugin for binary (ex: .puz)
	def read(self, path):
		text = ""
		with open(path, "r") as f:
			text = f.read()

		return text
	
	def write(self, path, content):
		with open(path, "w") as f:
			f.write(content)

		return
	
	# Main methods that read the file and parse
	def import_puzzle(self, file):
		puzzle = self.read(file)
		return self.parse(puzzle)
	
	# And serialize and write to file
	def export_puzzle(self, puzzle, file):
		text = self.serialize(puzzle)
		return self.write(file, text)