# XWORD - Converter

<hr>

**Warning**: It currently does not handle the .puz checksums and thus the output could be interpreted as invalid by some programs.

<hr>

This is a python library that is able to parse and serialize different crossword puzzle formats.

The three formats currently supported are:
 - `.puz`, the Across Lite format (binary)
 - `.json`, as used by the NYT ([detailed here](https://www.xwordinfo.com/JSON/))
 - `.json`, full internal data as represented internally in the library

## Installing

Run the following command in this folder to install it:
`pip install .`

## Usage

There are two main ways to use the program. You can either import directly from file and export the converted puzzle to a file again, or use the parsed `Puzzle` class to analyse and extract data from the puzzle for your own needs.

#### Importing and Exporting a puzzle

```python
import xword_converter as xword

# Import the puzzle to a Puzzle  object from a file
puzzle = xword.puz.import_file("puzzle.puz")
# And write the Puzzle object to file again
xword.json.export_file(puzzle, "puzzle.json")
```

If you already read the file somewhere and only want to parse it or if you want to import your own custom exporting logic, do the following:

```python
import xword_converter as xword

json_puzzle = { 
	"puzzle": "... data ..."
}

# Read the puzzle from a string
puzzle = xword.json_nyt.parse(json_puzzle)

# And serialize it again
xword.puz.serialize(puzzle)
```

The `Puzzle` object that is the output of parsing and serializing looks like this has the following attributes:

```json
{
    "grid": [
        "M",
        "E",
        "T",
        "R",
        "O",
		"Rest of the grid's squares..."
    ],
    "across_clues": [
        {
            "x": 0,
            "y": 0,
            "label": 1,
            "clue": "",
            "word": "METRO",
            "squares": [
                0,
                1,
                2,
                3,
                4
            ],
            "related_clues": []
        }
    ],
    "down_clues": [
        {
            "x": 0,
            "y": 0,
            "label": 1,
            "clue": "",
            "word": "TRAMS",
            "squares": [
                0,
                5,
                10,
                15
            ],
            "related_clues": []
        }
    ],
    "dimensions": [
        5,
        5
    ],
    "metadata": {
        "title": "Crosshare puzzle",
        "author": "uuid v4",
        "copyright": "Copyright uuid v4, all rights reserved",
        "notes": {
            "note": "Created on crosshare.org"
        }
    }
}
```