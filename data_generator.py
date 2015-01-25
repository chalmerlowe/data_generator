# Title: data_generator.py
# Usage: data_generator.py <input_file> <num_of_lines> <file_type> <output_file>
# Revision: 0.9
# Python version: 3.x
# Author: Chalmer Lowe 
# Date: 20150121
# Description: This script generates various files with random/semi-random 
#              data for use in classes and demonstrations.
# 
# TODO:
#   2) improve commenting so that the functions have built-in help
#   3) enable an option such that the user can skip writing a full-blown file 
#      and can instead write just a certain set of columns
#      i.e. can choose just name, or just name, email, lat & long columns
#   4) provide an option to include a header row
#   5) improve the usage component to produce a help file 
#   6) set up outputs for other file types...
#      * json
#      * xml
#      * pickle
#   7) add more columns?
#      * to/fm mac addr - need to consider pairing to ips?
#      * payload size (0-1000000) # FUNC is complete, not integrated yet.
#      * user agent string - need to consider pairing to ips?
#        > browser
#        > windows/mac/linux
#        > version
#   8) add an option to include/exclude corrupted data
#      * corrupted data -> NULL, blank lines, random gobbledy-gook
#      * enable the inclusion of some/all
#      * enable the use of threshholds: very corrupted/limited corruption
#   9) add an option to set the delimiter AND/OR include quoting

from random import choice, randint, random
import datetime
from datetime import datetime as dt
from collections import defaultdict

import sys

try:
    input_file = sys.argv[1]
    num_of_lines = int(sys.argv[2])
    file_type = sys.argv[3]
    out_file = sys.argv[4]

except IndexError:
    sys.exit('''
    data_generator produces data in multiple formats, including sql tables
    and csvs.
    Usage: data_generator.py <input_file> <num_of_lines> <file_type> <out_file>
    ''')

def create_email(fname, lname, domain):
    '''Creates an email address in the format first initial last name @ domain
    for example:
    bwayne@batman.org
    '''
    addr = '{}{}@{}'.format(fname[0], lname, domain)
    return addr

fin = open(input_file)
domain = fin.readline().strip()

names = defaultdict(str)

for line in fin:
    line = line.strip()
    fname, lname = line.split(' ')
    names[line] = create_email(fname, lname, domain)
        
def generate_ips():
    '''creates a list of strings that simulate compliant ip addresses.
    '''
    ips = []
    octets = []
    for x in range(30):
        for octet in range(4):
            octets.append(str(choice(range(1, 256))))
            
        ip = '.'.join(octets)
        ips.append(ip)
        octets = []
    return ips


ip_list = generate_ips()    

def create_payload_size():
    '''Generates a random payload size for the communication session.
    Ranges from 1 byte to 1000000 bytes
    '''
    size = choice(range(1, 1000001))
    return size

    
def create_tdelta():            # rename...
    '''creates a number that simulates a compliant timestamp.
    should produce incremental timestamps with a small, variable 
    separation from the previous timestamp. 
    '''
    digits = [-1, 0, 0, 0, 0, 0]      # this construct roughly equates to
                                      # a backwards shift of ~1 day for every 
                                      # six records. Add/remove zeroes to change
                                      # this
    increment = datetime.timedelta(choice(digits),
                             choice(range(1, 100)))
    return increment                             

    
def geo(min_lat, max_lat, min_long, max_long):
    '''creates a pair of numbers that simulate a geo-location with
    latitude and longitude based on the decimal degrees format:
    40.446 N 79.982 W
    For purposes of generating 'bounding box' puzzles/problems, this generator
    can output geos within a 'large' bounding box enabling a smaller
    bounding box to be selected out of the broader range of geos as part of the
    puzzle.
    '''
    lat_bounds = [min_lat, max_lat]
    lat = (random() * (max_lat - min_lat)) + min_lat
    lat = str(round(lat, 5))
    
    long_bounds = [min_long, max_long]
    long = (random() * (max_long - min_long)) + min_long
    long = str(round(long, 5))
    
    return lat, long


# The lat longs below create a bounding box around Liechtenstein 
# (why?, because!)
# 47.141667, 9.523333     

min_lat = 45
max_lat = 50
min_long = 7.5
max_long = 12.5

def create_outputs(num_of_lines, new_line=True):
    output = ''
    if new_line == True:
        new_line = '\n'
    else:
        new_line = ''
    curr_time = dt.now()
    outputs = []
    for line in range(num_of_lines):
        # generate a new line by calling all the appropriate funcs
        # and gathering the results into an output line
        
        name = choice(list(names.keys()))
        email = names[name]
        fmip = choice(ip_list)
        toip = choice(ip_list)
        tstamp = curr_time.strftime('%Y-%m-%dT%H:%M:%S')
        lat, long = geo(min_lat, max_lat, min_long, max_long)
        # print(name, email, fmip, toip, tstamp, lat, long)    #dbg
        output = ','.join([name, email, fmip, 
                           toip, tstamp, lat, long]) + new_line
        time_inc = create_tdelta()
        curr_time += time_inc
        outputs.append(output)
        output = ''
    return outputs

if file_type == 'csv':
    with open(out_file, 'w') as fout:
        outputs = create_outputs(num_of_lines)    
        print('Output length (csv):', len(outputs))
        for line in outputs:
            fout.write(line)
    fout.close()
    
elif file_type == 'sql':
    import sqlite3 as sql
    conn = sql.connect(out_file)
    cur = conn.cursor()
    try: 
        cur.execute('''CREATE TABLE superheroes (name text,
                                                 email text,
                                                 fmip text,
                                                 toip text,
                                                 datetime text,
                                                 lat text,
                                                 long text)''')
    except:
        pass

    outputs = create_outputs(num_of_lines, new_line=False)
    print('Output length (sql):', len(outputs))
    for line in outputs:
        name, email, fmip, toip, datetime, lat, long = line.split(',')
        cur.execute('''INSERT INTO superheroes VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (name, email, fmip, toip, datetime, lat, long))
    conn.commit()
    for n, l in cur.execute('''SELECT name, lat FROM superheroes LIMIT 200'''):
        print(n, l)
    conn.close()
