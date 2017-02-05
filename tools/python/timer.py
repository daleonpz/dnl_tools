#!/usr/bin/python2.7
###############################
#  T O   D O
###############################
# - close automatically
# - larger fonts
# - sound as output
# - add titles
# - multiset timer (future)

################################
#   I M P O R T S
################################
from Tkinter import *

import sys
import re
import getopt
################################
#   F U N C T I O N S
################################
def usage():
    print "Usage:"
    print "\t-h, --help\t\t\t: display help"
    print "\t-t, --time\t\t\t: set time following format 00:00" 

################################
#   C L A S S E S 
################################

# must not use time.sleep() since it blocks the app
class Countdown(Label):
        def __init__(self, parent, timer):
            t = map(int,re.split(":",timer))
            self.value = t[1] + t[0]*60
            t ="{:02d}:{:02d}".format(*divmod( self.value, 60)) 
            Label.__init__(self, parent, width=5, text=t)
            self._job_id = None

        def tick(self):
            self.value -= 1
            text = "{:02d}:{:02d}".format(*divmod(self.value, 60))
            self.configure(text=text)
            if self.value > 0:
                self._job_id = self.after(1000, self.tick)

        def start(self):
            if self._job_id is not None: return

            self.stop_requested = False
            self.after(1000, self.tick)

        def stop(self):
            self.after_cancel(self._job_id)
            self._job_id = None

class Application(Frame):
    def createWidgets(self,timer):
        label =  Countdown(self, timer)
        label.pack(side=TOP)
        
        label.start()

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack(side=LEFT)

    # SyntaxError: non-default argument follows default argument
    # thus, variable timer cannot be after master=None
    def __init__(self,timer, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets(timer)

################################
#   M A I N
################################
def main():
    
    try:
        opts, args = getopt.getopt(sys.argv[1:] , "ht:", ["time="]  )
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    if (opts == []):
        usage()
        sys.exit()
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ( '-t', '--time'):
            root = Tk()
            app = Application( arg, master=root)
            app.mainloop()
            root.destroy()
        else:
            assert False, "unhandled option"


if __name__ == "__main__":
    main()

