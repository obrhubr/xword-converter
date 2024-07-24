import argparse

import converter as xword

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		prog='Crossword Converter',
		description='Convert different crossword puzzle formats into others.',
	)

	parser.add_argument('-i', '--input')
	parser.add_argument('-if', '--input-format')

	parser.add_argument('-o', '--output')
	parser.add_argument('-of', '--output-format')

	parser.add_argument('-l', '--list', help="List all available formats.", action='store_true')

	args = parser.parse_args()

	converter = xword.Converter()

	if args.list:
		print(xword.list_formats())

	xword.convert(args.input, args.input_format, args.output, args.output_format)