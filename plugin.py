class Plugin:
	def __init__(self):
		return
	
	def parse(self, puzzle_text):
		return
	
	def export(self, puzzle):
		return
	
	def write(self, path, content):
		with open(path, "w") as f:
			f.write(content)

		return
	
	def read(self, path):
		text = ""
		with open(path, "r") as f:
			text = f.read()

		return text