#!/usr/bin/python3

import argparse, random, string, sys

E_FLAG = False
I_FLAG = False
R_FLAG = False
N_FLAG = False
O_FLAG = False
H_FLAG = False

class Shuf:
	def __init__(self):
		pass

	def createParser(self):
		# Initialize parser
		return argparse.ArgumentParser(description = 'shuf.py')
		
	def setOptionals(self, parser):
		pass
		# Add optional arguments
		parser.add_argument("-e", "--echo", action = "store_true", help = "set input as individual element")
		parser.add_argument("-i", "--input-range", action = "store_true", help = "set range for unsigned integer")
		parser.add_argument("-r", "--repeat", action = "store_true", help = "repeat the set of elements")
		parser.add_argument("-n", "--head-count", dest = "headcount", action = "store", help = "print only set count times", metavar='\b')
		parser.add_argument("-o", "--output", action = "store", help = "set output file", metavar='\b')
		
	def checkOptions(self, argument):
		# Checks for optional -e
		if "-e" in argument or "--echo" in argument:
			# Checks for -i and -e combination
			if "-i" in argument or "--input-range" in argument:
				sys.exit("Cannot combine -e and -i")
			else:
				global E_FLAG 
				E_FLAG = True
				
		# Checks for optional -i
		if "-i" in argument or "--input-range" in argument:
			global I_FLAG 
			I_FLAG = True
			
		# Checks for optional -r
		if "-r" in argument or "--repeat" in argument:
			global R_FLAG 
			R_FLAG = True
			
		# Checks for optional -n
		if "-n" in argument or "--head-count" in argument:
			global N_FLAG 
			N_FLAG = True
			
		# Checks for optional -o
		if "-o" in argument or "--output" in argument:
			global O_FLAG 
			O_FLAG = True
			
		# Checks for optional -h
		if "-h" in argument or "--help" in argument: 
			global H_FLAG
			H_FLAG = True
			
	def setInput(self, parser):
		# Sets -e for main input
		if E_FLAG:
			parser.add_argument('operand', nargs = '+')
		# Sets -i for main input
		elif I_FLAG:
			parser.add_argument('operand')
		# Sets file input for main input
		else:
			parser.add_argument('operand', type = argparse.FileType('r'), help = "set file")
			
	def O_Option(self, input, output):
		# Opens file and writes the output to file
		file = open(output, "w+")
		for i in range(0, len(input)):
			file.write(input[i] + "\n")
		file.close()
			
	def R_Option(self, input, num):
		# Returns a random element from the list
		input = random.choices(input, k = int(num))
		return random.sample(input, len(input))
			
	def I_Option(self, input):
		# Removes hyphen from input
		input = input.replace('-', ' ')
		# Creates a list of integers split from spaces
		input = [int(n) for n in input.split()]
		# Creates a new list with integers from range 
		num_list = list(range(input[0], input[1] + 1))
		
		return num_list
		
	def N_Option(self, input, args):
		# Initialize new list
		new_list = []
		# Creates a new list up to range in list
		for i in range(0, int(args)):
			new_list.append(input[i])
			
		return new_list
		
	def OptionInitiate(self, shuffle, args):
		# I_Flag operation
		if I_FLAG == True:
			# Creates list of integer range
			shuffle = self.I_Option(shuffle)
			# Integer list to string list
			shuffled_list = [str(i) for i in shuffle]
			# Shuffle list
			shuffle = self.shuffleList(shuffled_list)
			
		# R_Flag operation
		if R_FLAG == True:
			# Check for N flag to cut list
			if N_FLAG == True:
				shuffle = self.R_Option(shuffle, args.headcount)
			else: 
			# If no N flag to cut infinite repetition
				while(1):
					# Print a random element in the list infinitely
					print(random.choice(shuffle))
						
		# N_Flag operation
		if N_FLAG == True:
			# Shuffle list
			shuffle = self.shuffleList(shuffle)
			# Cut list to count elements
			shuffle = self.N_Option(shuffle, args.headcount)
			
		# O_Flag operation
		if O_FLAG == True:
			# Set output
			self.O_Option(shuffle, args.output)
			
		return shuffle	
			
	def makeList(self, file_arg):
		# Make list for input separated by spaces
		if E_FLAG == True or I_FLAG == True:
			input_list = file_arg
		# Make list for input separated by new lines
		else:		
			input_list = file_arg.read().splitlines() 
		
		return input_list
		
	# Shuffle list function
	def shuffleList(self, list):
		# Returns a shuffled list
		shuffled_list = list.copy()
		return random.sample(shuffled_list, len(shuffled_list))
			
	# Simple print function 
	def printList(self, list):
		for element in list:
			print(element)
			
	# Cutom help command
	def usage_msg(self):
		print("Usage: python3 shuf.py [OPTION]... [FILE]")
		print("   or: python3 shuf.py -e [OPTION]... [ARG]...")
		print("   or: python3 shuf.py -i LO-HI [OPTION]...")
		
		print("\nWrite a random permutation of the input lines to standard output")
		print("With no FILE, or when FILE is -, read standard input.\n")
		
		print("-e, --echo                   treats each ARG as an input line")
		print("-i, --input-range = lo-hi    treats each num lo through hi as input line")
		print("-n, --head-count = count     output at most count lines")
		print("-o, --output=FILE            write result to FILE instead of standard output")
		print("-r, --repeat                 output lines are repeated")
		print("-h, --help                   opens up this help screen")
		
		sys.exit("")
	
def main():
	# Create object for class Shuf
	shuf = Shuf()
	
	# Create parser
	parser = shuf.createParser()
	
	# Set optionals
	shuf.setOptionals(parser)
	
	# Checks for input after first invokation
	if len(sys.argv) > 1:
		# Convert system input to string
		shuf.checkOptions(sys.argv)
	# No arguments
	else:
		print("No arguments")
		
	# Checks for H_FLAG
	if H_FLAG == True:
		shuf.usage_msg()
		
	# Set the input for shuf
	shuf.setInput(parser)
		
	# Read arguments from command line, allows access to input args.operand
	args = parser.parse_args()
	
	# Creates list file from input file type
	input_list = shuf.makeList(args.operand)
	
	# Shuffles list
	if I_FLAG == False:
		input_list = shuf.shuffleList(input_list)
	
	# Adds options
	output_list = shuf.OptionInitiate(input_list, args)
	
	# Prints list
	shuf.printList(output_list)
	
		
if __name__ == "__main__":
	main()