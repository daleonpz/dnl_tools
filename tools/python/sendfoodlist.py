#!/usr/bin/python2.7

import gmailapi

###################################
#   F u n c t i o n s
###################################
def request_list():
    print 'Add items to your list:'
    print "write 'done' when your list is complete:"
    item = raw_input('>> ')
    my_list = ''
    while (item != 'done'):
        my_list += (' - ' + item + '\n')
        item = raw_input('>> ')

    return my_list

######################################
#      M A I N
######################################

gm = gmailapi.Gmail_api()

gm.set_headers("Shopping List", "daleonpz@gmail.com", "plain")

shopping_list = request_list()
gm.set_body( shopping_list )

timer = raw_input('Set alarm, 24Hrs format >> ')
gm.set_alarm(timer)

