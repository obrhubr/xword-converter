class Puzzle:
	# grid: list representing the filled out crossword. Black squares are "."
	# across_clues: list of clues for words across, { x: 0, y: 0, label: 0, word: "", clue: "", squares: [0, 10, 20], related_clues: [11, 12] }
	# down_clues: same as across_clues
	# dimensions: tuple (x, y) size
	# metadata: dict with all metadata, but always: title, author, copyright, notes
	def __init__(self, grid, across_clues, down_clues, dimensions, metadata):
		self.grid = grid
		self.across_clues = across_clues
		self.down_clues = down_clues
		self.dimensions = dimensions
		self.metadata = metadata
		
		return
	
	def all_clues(self):
		return self.across_clues + self.down_clues