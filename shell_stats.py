#!/usr/bin/python2.7

import re # Regex

#log = [ line.rstrip('\n') for line in  open('/var/log/pacman.log','r')]

#tags = []
#for line in log:
#    tags += re.findall('\[[A-Z\-]+\]', line) 
#tags = list(set(tags))

#print tags


file = open('/var/log/pacman.log','r').read()

# get the metadata and tags
metadata = re.findall('\[[0-9\-\s:]+\]\s+\[[A-Z\-]+\]', file)
tags = re.findall('\[[A-Z\-]+\]', file)

counts = [  tags.count(x)  for x in  list(set(tags))  ]
tags = list(set(tags))

dictionary = dict(zip(tags, counts))

print dictionary 

#os.popen('HISTTIMEFORMAT="%d/%m/%y %T "').read()

import subprocess
#p = subprocess.Popen(["history","16"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
p = subprocess.Popen(["ps","-a"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
#(output , err) = p.communicate()
#print output
for line in p.stdout.readlines():
    print line
retval = p.wait()

import commands
print commands.getstatusoutput('history')
