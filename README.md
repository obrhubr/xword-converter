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

converter = xword.Converter()

# Import the puzzle to a Puzzle  object from a file
puzzle = converter.import_puzzle("puzzle.puz", "puz")
# And write the Puzzle object to file again
converter.export_puzzle(puzzle, "puzzle.json", "json")
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
        "title": "Crossword puzzle",
        "author": "obrhubr",
        "copyright": "Copyright notice",
        "notes": {
            "note": "This is a note."
        }
    }
}
```
