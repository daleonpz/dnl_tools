#!/usr/bin/python2.7

from sys import argv

i = """
################################
#   I M P O R T S
################################
"""

f = """
################################
#   F U N C T I O N S
################################
"""

c = """
################################
#   C L A S S E S 
################################
"""

m = """
################################
#   M A I N
################################
"""

script, filename = argv

out_file = open(filename, 'w')
out_file.write("#!/usr/bin/python2.7")
out_file.write(i + f + c + m)
out_file.close()

