from plugin import Plugin
from puzzle import Puzzle
import json

class Plugin(Plugin):
	def __init__(self):
		return

	def parse(self, puzzle_text):
		puzzle = json.loads(puzzle_text)

		return Puzzle(
			puzzle["grid"], 
			puzzle["across_clues"], 
			puzzle["down_clues"],
			puzzle["dimensions"],
			puzzle["metadata"]
		)

	def export(self, puzzle):
		puzzle_dict = {
			"grid": puzzle.grid,
			"across_clues": puzzle.across_clues,
			"down_clues": puzzle.down_clues,
			"dimensions": puzzle.dimensions,
			"metadata": puzzle.metadata
		}

		return json.dumps(puzzle_dict, indent=4)