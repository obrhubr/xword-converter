from plugin import Plugin
from puzzle import Puzzle
import json

class Plugin(Plugin):
	def __init__(self):
		return
	
	def word_from_squares(self, squares, grid):
		word = ""
		for square in squares:
			word += grid[square]
		return word


	def parse(self, puzzle_text):
		puzzle = json.loads(puzzle_text)

		# Parse grid
		grid = []
		for cell in puzzle["body"][0]["cells"]:
			if cell:
				if "answer" in cell:
					grid += [cell["answer"]]
				elif "moreAnswers" in cell:
					# Take longest string = rebus from moreAnswers
					answers = cell["moreAnswers"]["valid"]
					grid += [max(answers, key=len)]
				elif "clues" in cell:
					grid += "."
				else:
					raise Exception("No answer in grid cell.")
			else:
				grid += ["."]

		across_clues = []
		down_clues = []

		for clue in puzzle["body"][0]["clues"]:
			if len(clue["text"]) > 1:
				raise  Exception("Clue text longer than 1.")
			
			relatives = []
			if "relatives" in clue:
				relatives = clue["relatives"]

			first_cell = clue["cells"][0]
			x = first_cell % puzzle["body"][0]["dimensions"]["width"]
			y = first_cell // puzzle["body"][0]["dimensions"]["width"]

			# read either plain or formatted clue
			clue_text = ""
			if "plain" in clue["text"][0]:
				clue_text = clue["text"][0]["plain"]
			elif "formatted" in clue["text"][0]:
				clue_text = clue["text"][0]["formatted"]
				clue_text = clue_text.replace("&nbsp;", " ")
			else:
				raise Exception("Could not read text from NYT clue")

			if clue["direction"] == "Across":
				across_clues += [{ 
					"x": x,
					"y": y,
					"label": int(clue["label"]),
					"clue": clue_text,
					"word": self.word_from_squares(clue["cells"], grid),
					"squares": clue["cells"],
					"related_clues": relatives
				}]
			elif clue["direction"] == "Down":
				down_clues += [{
					"x": x,
					"y": y,
					"label": int(clue["label"]),
					"clue": clue_text,
					"word": self.word_from_squares(clue["cells"], grid),
					"squares": clue["cells"],
					"related_clues": relatives
				}]
			elif clue["direction"] == "Diagonal":
				# TODO: Ignore diagonals
				pass
			elif clue["direction"] == "Around":
				# TODO: Ignore around
				pass
			elif clue["direction"] == "Road":
				# TODO: Ignore road
				pass
			elif clue["direction"] == "Diamond":
				# TODO: Ignore road
				pass
			elif clue["direction"] == "Heart":
				# TODO: Ignore road
				pass
			else:
				raise Exception("Empty clue in NYT puzzle json.")
			
		notes = {
			"published": puzzle["publicationDate"]
		}
		if "editor" in puzzle:
			notes["editor"] = puzzle["editor"],

		return Puzzle(
			grid,
			across_clues, 
			down_clues,
			(puzzle["body"][0]["dimensions"]["width"], puzzle["body"][0]["dimensions"]["height"]),
			{
				"author": puzzle["constructors"][0],
				"copyright": puzzle["copyright"],
				"notes": notes
			}
		)

	def export(self, puzzle):
		return