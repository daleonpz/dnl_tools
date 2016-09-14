#!/usr/bin/python2.7

import re # Regex

log = [ line.rstrip('\n') for line in  open('/var/log/pacman.log','r')]

tags = []
for line in log:
    tags += re.findall('\[[A-Z\-]+\]', line) 
tags = list(set(tags))

print tags


file = open('/var/log/pacman.log','r')
# get the dates and tags
tags = re.findall('\[[0-9\-\s:]+\]\s+\[[A-Z\-]+\]', file.read())

print set(tags)

file.close ()
