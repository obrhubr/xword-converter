import argparse
import importlib
from os import listdir
from os.path import isfile, join

from util import *

def list_formats():
	onlyfiles = [f for f in listdir(join("plugins")) if isfile(join("plugins", f))]
	return onlyfiles

def main(input_path, input_format, output_path, output_format):
	try:
		input_format_lib = importlib.import_module("plugins." + input_format)
		output_format_lib = importlib.import_module("plugins." + output_format)

		input_plugin = input_format_lib.Plugin()
		output_plugin = output_format_lib.Plugin()
	except:
		print("Could not find requested file format")
		return False

	input_file = input_plugin.read(input_path)
	parsed = input_plugin.parse(input_file)
	
	output_file = output_plugin.export(parsed)
	output_plugin.write(output_path, output_file)

	return True

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

	if args.list:
		print(list_formats())

	main(args.input, args.input_format, args.output, args.output_format)