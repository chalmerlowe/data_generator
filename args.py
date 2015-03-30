# Title:
# Filename:
# Usage: 
# Description:
# Author:
# Version:
# Python Revision:
# TO DO:
# 
#---------------------------------------------------------

import argparse
import sys

parser = argparse.ArgumentParser(
    description='Generate pseudorandom data for use in teaching and puzzles',
    epilog='Add epilog txt here.',
    formatter_class=argparse.RawTextHelpFormatter,
    prog='data_generator')
    
parser.add_argument('infile', type=argparse.FileType('r'), default=sys.stdin, help='''The input file to draw names from

''')

parser.add_argument('outfile', help='''The output filename to assign to the file that stores the results

''')

parser.add_argument('-n', '--numlines', default=10, help='''Set the number of lines to output. The default is 10

''')

parser.add_argument('-f', '--filetype', default='csv', choices=['csv', 'sql', 'json', 'xml', 'pickle'], help='''Identify an output filetype format for the results. The default is csv

''')

parser.add_argument('-c', '--columns', default='all', nargs='*', choices=['all', 'n', 'e', 'f', 't', 's', 'd', 'l', 'o', 'p'], help='''Choose the desired columns. The available options and columns include:
all = all columns

OR select from any mixture of the following:
n = name, 
e = email, 
f = from ip,
t = to ip,
s = source mac,
d = destination mac,
l = latitude,
o = longitude,
p = payload size.

Separate each option by a space:
-c all
-c n e f t
-c l o p
 
''')

parser.add_argument('-r', '--headerrow', default='False', choices=['True', 'False'], help='''Provide a header row based on selected columns. A value of True will include a header row. The default is False.

''')


parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.9')

args = parser.parse_args()



if args.infile:
    print('infile:', args.infile)
    for line in args.infile:
        print(line.strip())
    
if args.outfile:
    print('outfile:', args.outfile)
    
if args.filetype:
    print('filetype:', args.filetype)
    
if args.numlines:
    print('numlines:', args.numlines)        
    
if args.columns:
    print('column:', args.columns)
    if args.columns == 'all':
        print('all')
    else:
        # columns = list(args.columns)
        for col in args.columns:
            print(col)

if args.headerrow and args.columns:
    print('header:', args.headerrow)
    print('desired cols:', args.columns)
    if args.headerrow == 'False':
        print('will NOT include header row')
    else:
        print('will include header row')
    

    
# if args.filetype:
#     print('filetype:', args.filetype)











    