import io
import re
import copy

from xword_converter.plugin import Plugin
from xword_converter.puzzle import Puzzle

class Plugin(Plugin):
	def __init__(self):
		return
	
	def until_null(self, stream):
		text = ""
		byte = stream.read(1)
		while byte[0] != 0:
			try:
				text += byte.decode("latin1")
			except:
				text += "."
			byte = stream.read(1)

		return text
	
	def parse_file(self, puzzle_stream):
		# read checksum
		puzzle_stream.read(2)

		# magic number
		magic = puzzle_stream.read(11).decode("utf-8")
		assert puzzle_stream.read(1) == b"\x00"
		if magic != "ACROSS&DOWN":
			raise Exception(".puz file not valid.")
		
		# read checksums
		puzzle_stream.read(30)

		# read puzzle dimensions
		dimensions = (
			int.from_bytes(puzzle_stream.read(1), byteorder="big"), 
			int.from_bytes(puzzle_stream.read(1), byteorder="big")
		)
		n_clues = int.from_bytes(puzzle_stream.read(2), byteorder="little")

		# read checksums
		puzzle_stream.read(4)

		# Parse grids
		grid_string = puzzle_stream.read(dimensions[0] * dimensions[1]).decode("ascii")
		player_string = puzzle_stream.read(dimensions[0] * dimensions[1]).decode("ascii")

		# Read metadata
		metadata = {
			"title": self.until_null(puzzle_stream),
			"author": self.until_null(puzzle_stream),
			"copyright": self.until_null(puzzle_stream),
			"notes": {}
		}

		# Parse clues
		clues = []
		while len(clues) < n_clues:
			clues += [self.until_null(puzzle_stream)]

		# Read in notes at the end
		metadata["notes"]["note"] = self.until_null(puzzle_stream)
		
		# Read in extra information
		extras = {
		}

		while puzzle_stream.tell() > 8:
			title = puzzle_stream.read(4).decode("latin1")
			length = int.from_bytes(puzzle_stream.read(2), byteorder="little")
			if length == 0:
				break

			# checksum
			puzzle_stream.read(2)

			# read in data
			data = puzzle_stream.read(length)

			# skip until next char
			self.until_null(puzzle_stream)

			if title == "GRBS":
				extras["GRBS"] = data
			elif title == "RTBL":
				extras["RTBL"] = data.decode("latin1")
			elif title == "GEXT":
				extras["GEXT"] = data

		return grid_string, dimensions, clues, extras, metadata
	
	def parse_grid(self, grid_string):
		grid = []
		for c in grid_string:
			grid += [c]

		return grid
	
	def parse_clues(self, grid, dimensions, clues_list):		
		def word_from_squares(squares, grid):
			word = ""
			for square in squares:
				word += grid[square]
			return word
		
		# get squares that belong to a clue
		def get_squares(c_num, direction, grid, dimensions):
			squares = []

			x = c_num % dimensions[0]
			y = c_num // dimensions[0]

			if direction == "across":
				while (c_num < len(grid)) and (grid[c_num] != "."):
					squares += [c_num]

					if x == dimensions[0] - 1:
						break

					# move to next square, right
					c_num += 1
					x = c_num % dimensions[0]
			else:
				while (c_num < len(grid)) and (grid[c_num] != "."):
					squares += [c_num]

					if y == dimensions[1] - 1:
						break

					# move to next square, down
					c_num += dimensions[0]
					y = c_num // dimensions[0]

			return squares

		# Create clue lists for both directions
		across = []
		down = []

		# Assign labels to the clues
		label = 1
		inc = 0

		n = 0
		for i in range(0, dimensions[0] * dimensions[1]):
			if grid[i] == ".":
				continue

			# Reset label increase
			inc = 0

			if i % dimensions[0] == 0 or grid[i - 1] == ".":
				squares = get_squares(i, "across", grid, dimensions)
				across += [{
					"x": i % dimensions[0],
					"y": i // dimensions[0],
					"label": label,
					"clue": clues_list[n],
					"word": word_from_squares(squares, grid),
					"squares": squares,
					"related_clues": []
				}]
				n += 1
				inc = 1

			if i < dimensions[0] or grid[i - dimensions[0]] == ".":
				squares = get_squares(i, "down", grid, dimensions)
				down += [{
					"x": i % dimensions[0],
					"y": i // dimensions[0],
					"label": label,
					"clue": clues_list[n],
					"word": word_from_squares(squares, grid),
					"squares": squares,
					"related_clues": []
				}]
				n += 1
				inc = 1

			label += inc

		return across, down
				
	def parse_extras(self, extras, grid):
		if "RTBL" in extras and "GRBS" in extras:
			rebus_table = {}
			# remove whitespace from RBTL
			re.sub(r"\s+", "", extras["RTBL"])
			# split on ';'
			for r in extras["RTBL"][:-1].split(";"):
				rebus_table[r.split(":")[0].strip()] = r.split(":")[1]

			for i in range(len(extras["GRBS"])):
				n = extras["GRBS"][i]
				if n != 0:
					grid[i] = rebus_table[str(n - 1)]

		# TODO: Ignore extra information like highlights and circles for now

		return grid

	def parse(self, puzzle_stream):
		# Parse file into information
		grid_string, dimensions, clues_list, extras, metadata = self.parse_file(puzzle_stream)

		# Parse grid
		grid = self.parse_grid(grid_string)

		# Parse extra information
		grid = self.parse_extras(extras, grid)

		# Parse clues
		across_clues, down_clues = self.parse_clues(grid, dimensions, clues_list)

		return Puzzle(
			grid,
			across_clues,
			down_clues,
			dimensions,
			metadata
		)
	
	def write_header(self, stream, puzzle):
		# TODO: Correctly compute checksum
		stream.write(b"\x00" * 2)

		# Write magic number
		stream.write("ACROSS&DOWN".encode("utf-8"))
		stream.write(b"\x00")

		stream.write(b"\x00" * 2)
		stream.write(b"\x00" * 8)

		# Write version
		stream.write("2.0".encode("utf-8"))
		stream.write(b"\x00")

		stream.write(b"\x00" * 2)
		stream.write(b"\x00" * 2)
		stream.write(b"\x00" * 12)

		# write dimensions
		stream.write(puzzle.dimensions[0].to_bytes(1, byteorder='big'))
		stream.write(puzzle.dimensions[1].to_bytes(1, byteorder='big'))

		# write number of clues
		stream.write(
			(len(puzzle.across_clues) + len(puzzle.down_clues))
			.to_bytes(2, byteorder='little')
		)
		
		# Write puzzle type
		stream.write(b"\x00" * 2)
		stream.write(b"\x00" * 2)
	
	def write_boards(self, stream, puzzle):
		for cell in puzzle.grid:
			stream.write(cell[0].encode("ascii"))
		for cell in puzzle.grid:
			if cell != ".":
				stream.write("-".encode("ascii"))
			else:
				stream.write(cell.encode("ascii"))
	
	def write_metadata(self, stream, puzzle):
		# Write title
		stream.write(puzzle.metadata["title"].encode("latin1"))
		stream.write(b"\x00")
		# Write author
		stream.write(puzzle.metadata["author"].encode("latin1"))
		stream.write(b"\x00")
		# Write author
		stream.write(puzzle.metadata["copyright"].encode("latin1"))
		stream.write(b"\x00")
	
	def write_clues(self, stream, puzzle):
		clues = copy.deepcopy(puzzle.all_clues())

		# Sort clues in ascending order
		clues.sort(key=lambda x: x["label"] * 2)

		for clue in clues:
			stream.write(clue["clue"].encode("latin1"))
			stream.write(b"\x00")
	
	def write_notes(self, stream, puzzle):
		if "notes" in puzzle.metadata:
			for _, note in puzzle.metadata["notes"].items():
				stream.write(note.encode("latin1"))
		stream.write(b"\x00")
	
	def write_extras(self, stream, puzzle):
		# Write GRBS
		stream.write("GRBS".encode("latin1"))
		# Write length
		stream.write((puzzle.dimensions[0] * puzzle.dimensions[1]).to_bytes(2, byteorder="little"))
		# Checksum
		stream.write(b"\x00" * 2)

		rebus_list = []
		for cell in puzzle.grid:
			if len(cell) > 1:
				# Check if rebus already in list
				if not cell in rebus_list:
					rebus_list += [cell]

				# Write position of rebus in RTBL to GRBS board
				stream.write((rebus_list.index(cell) + 2).to_bytes(1, byteorder="little"))
			else:
				stream.write(b"\x00")

		# terminate GRBS
		stream.write(b"\x00")

		# Write RTBL
		stream.write("RTBL".encode("latin1"))

		rtbl = ""
		# create RTBL string
		for idx, rebus in enumerate(rebus_list):
			# write rebus to file, with space in front of rebus number if only one digit
			rtbl += f"{'{:>2}'.format(idx + 1)}:{rebus};"

		# Write length
		stream.write((len(rtbl)).to_bytes(2, byteorder="little"))
		# Checksum
		stream.write(b"\x00" * 2)

		stream.write(rtbl.encode("latin1"))

		# terminate RTBL
		stream.write(b"\x00")


	def serialize(self, puzzle):
		puzzle_stream = io.BytesIO()

		# write header
		self.write_header(puzzle_stream, puzzle)

		# write boards
		self.write_boards(puzzle_stream, puzzle)

		# write metadata
		self.write_metadata(puzzle_stream, puzzle)

		# write clues
		self.write_clues(puzzle_stream, puzzle)

		# write notes
		self.write_notes(puzzle_stream, puzzle)

		# Write extras
		# Check if there is any Rebus
		if any(len(s) > 1 for s in puzzle.grid):
			self.write_extras(puzzle_stream, puzzle)

		return puzzle_stream
	
	def write(self, path, content):
		with open(path, "wb") as f:
			f.write(content.getbuffer())

		return
	
	def read(self, path):
		return io.open(path, "rb", buffering = 0)