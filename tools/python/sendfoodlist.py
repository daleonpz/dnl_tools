#!/usr/bin/python2.7

import gmailapi

######################################
#      M A I N
######################################

gm = gmailapi.Gmail_api()
gm.get_data()
gm.set_alarm()

