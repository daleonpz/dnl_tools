#!/usr/bin/python2.7
###############################
#  T O   D O
###############################
# - multiset timer (future)

################################
#   I M P O R T S
################################
from Tkinter import *

import sys
import re
import getopt
import pygame
import argparse

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
            Label.__init__(self, parent, width=5, text=t, font=('Helvetica','20'))
            self._job_id = None
            pygame.init()
            pygame.mixer.music.load("/home/dnl/Documents/gitStuff/dnl_tools/tools/python/timer.wav")

        def tick(self):
            self.value -= 1
            text = "{:02d}:{:02d}".format(*divmod(self.value, 60))
            self.configure(text=text)
            if self.value > 0:
                self._job_id = self.after(1000, self.tick)

            if self.value == 0: self.stop_loop()

        def start(self):
            if self._job_id is not None: return

            self.stop_requested = False
            self.after(1000, self.tick)

        def stop_loop(self):
            if not( self.stop_requested ):
                pygame.mixer.music.play()
                self.after(5000, self.stop_loop)

class Application(Frame):
    def createWidgets(self, timer, header):
        label =  Countdown(self, timer)
        label.config( height = 2) 
        label.pack(side=LEFT)
        label.start()

        title = Label(self, text=header.upper(), font=('Helvetica','20', 'bold'));
        title.config( height = 2 )
        title.pack(side=TOP)

        self.STOP = Button(self)
        self.STOP["text"] = "STOP / QUIT"
        self.STOP["command"] =  self.quit
        self.STOP.config( height = 2, width = 20 )
        self.STOP.pack(side=LEFT)

    # SyntaxError: non-default argument follows default argument
    # thus, variable timer cannot be after master=None
    def __init__(self,timer, header, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets(timer, header)

################################
#   M A I N
################################
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("time", help="set time following format 00:00")
    parser.add_argument("-H","--header", help="task header", default="TASK")

    args = parser.parse_args()

    root = Tk()
    root.title("T I M E R")
    app = Application( args.time, args.header,  master=root)
    app.mainloop()
    root.destroy()

if __name__ == "__main__":
    main()

