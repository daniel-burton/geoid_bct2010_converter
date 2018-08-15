import csv, argparse

#PURPOSE: take a CENSUS TRACT census file from american factfinder and append a
#column with NYC DCP's BCT2010 numbers for better joining with GIS files, takes
#an 11-digit geoid as input. Originally done with sys.args, now updated to use
#argparse. Not sure if actually better to use argparse. But def less opaque to me

#usage example:
#C:\python27\ArcGIS10.3\python.exe C:\Users\d_burton\Desktop\python\geoid_translator.py C:\Users\d_burton\Desktop\censusfile.csv
#really running over the 80 character limit with these windows file paths ; _ ;

def bct_translate(geoid):
    """take the 11 digit geoid and turn it into a DCP boro code"""
    boros = {"061":"1", "005":"2", "047":"3", "081":"4", "085":"5"}
    #dictionary that associates GEOID county codes to boro codes
    return boros[geoid[3:6]]

parser = argparse.ArgumentParser(description="""Translate 11-digit Census Tract
                                 GEOID into a NYC-DCP BCT2010 number for better
                                 joining with GIS or Excel files""")
#create argument parser "parser," translates command line args into variables

parser.add_argument("input_file", help = """provide the input file, Census Bureau
                                            data at the tract level""")
default_output = "bct_translator_output.csv"
parser.add_argument("output_file", nargs = '?', help = """provide output file, default is
                                            (input_file)_bct_output.csv""",
                                            default = default_output)
#second positional argument is output file, else default value

args = parser.parse_args()

input_reader = csv.reader(open(args.input_file))
#create reader, an iterable that returns next line every time called
output_writer = csv.writer(open(args.output_file,'w'),dialect='excel')

labels = next(input_reader)  #first row in csv is column labels
labels.append("bct2010")  #add column for bct2010
output_writer.writerow(labels)  #write row to output

print("""Creating a copy of {0} with BCT2010 added in last column,
        saving as {1}\n""".format(args.input_file, args.output_file))

for tract in input_reader:
    #note, will start from second row since first row was read above
    geoid = tract[1] #2nd column is geoid
    tract.append(bct_translate(geoid) + geoid[-6:])
    #new column is boro code + last 6 digits of geoid
    output_writer.writerow(tract)
    #write full row with new column to the output file
