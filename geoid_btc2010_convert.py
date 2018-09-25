import csv, argparse, sys

def bct_translate(geoid):
    """take the 11 digit geoid and turn it into a DCP boro code using a dictionary"""
    boros = {"061":"1", "005":"2", "047":"3", "081":"4", "085":"5"}
    try:
	return boros[geoid[2:5]]
    except KeyError:
	print("Key Error! Unknown county: " geoid)
	return "Error "

#create command line arg parser, assign command line arguments with defaults for input and output files
parser = argparse.ArgumentParser(description = ("Translate 11-digit Census Tract GEOID into a"
                                                " NYC-DCP BCT2010 number for better joining with"
                                                " GIS or Excel files"))
parser.add_argument("input_file", help = ("provide the input file, Census Tract data"))
parser.add_argument("output_file", nargs = "?", help = ("provide output file, default is"
                                                        " bct_translator_output.csv"),
                                                        default = "bct_translator_output.csv")
parser.add_argument("--column", "-c", help = ("which column in csv is geoid? Usually in census bureau"
					" files it is 1. Note column indexes start with zero."),
					default = 1, type = int, nargs = "?")
args = parser.parse_args()


#now create csv reader and writer iterators
input_reader = csv.reader(open(args.input_file))

if sys.platform == "win32": #to deal with mysterious windows csv error
    output_writer = csv.writer(open(args.output_file,'wb'))
else:
    output_writer = csv.writer(open(args.output_file,'w'))

labels = next(input_reader)
labels.append("bct2010")
output_writer.writerow(labels)  #write label row to output

print(("Creating a copy of {0} with BCT2010 added in last column,"
    " saving as {1}\n").format(args.input_file, args.output_file))

#loop through the whole input csv, add the bct2010, output
for tract in input_reader:
    geoid = tract[args.column]
    tract.append(bct_translate(geoid) + geoid[-6:])
    output_writer.writerow(tract)
