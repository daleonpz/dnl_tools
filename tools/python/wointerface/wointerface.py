#!/usr/bin/python2.7
###############################
#  T O   D O
###############################

################################
#   I M P O R T S
################################
import Tkinter as tk

import sys
import re
import getopt
import pygame
import argparse
import time

################################
#   F U N C T I O N S
################################
def sequence(*args):
    for function in args:
        function
################################
#   C L A S S E S 
################################
class Countdown():
        def __init__(self, timer, frame):
            t = map(int,re.split(":",timer))
            self.value = t[1] + t[0]*60
            self.initvalue = self.value
            t ="{:02d}:{:02d}".format(*divmod( self.value, 60)) 

            self.label = tk.Label(frame, width=5, text=t, font=('Helvetica','20'))
            pygame.init()
            pygame.mixer.music.load("/home/dnl/Documents/gitStuff/dnl_tools/tools/python/timer.wav")

        def tick(self):
            self.value -= 1
            t = "{:02d}:{:02d}".format(*divmod(self.value, 60))
            self.label.configure(text=t)
            if self.value > 0:
                self.label.after(1000, self.tick)

            if self.value == 0: self.stop_loop()

        def start(self):
            self.label.after(1000, self.tick)

        def stop_loop(self):
            pygame.mixer.music.play()
            t ="{:02d}:{:02d}".format(*divmod( self.initvalue, 60)) 
            self.label.configure(text = t)
            self.value = self.initvalue 

class woToObject(object):
    def __init__(self, workout_file, master):
        self.master = master

        infile = open(workout_file)
        rawtext = infile.read()
        infile.close()
        self.superset = re.split("\n\n",rawtext)

        self.frame = tk.Frame(master)
        self.frame.grid()
        self.callGOWidget()

    def toObject(self):
        self.frame.destroy()
        struct = []
        l = len(self.superset)
        self.count = 0
        self.setcount = 0
        
        self.repInstance(0, l) 
            

    def repInstance(self, i, t):
        self.frame = tk.Frame(self.master) # new frame
        self.frame.grid()

        sets =  re.split("\n\* ",self.superset[i])
        ssrep = re.findall("[0-9:]+", sets[0] ) # superset rep
            #  [ rep , break] , check this part, later ;)
        rset = [ re.split("\n",x) for x in sets[1:] ]# set reps
            #  [ ex , rep, break ]

        numberofsets = int(ssrep[0])
        
        tk.Label(self.frame , text = "Superset " + str(i+1) + "/" + str(t) ).grid(
                    row=0, column=0, columnspan=numberofsets  )

        ssbreakLabel = Countdown("00:02", self.frame)
            # possible bug, when ssrep[0] = 0
        ssbreakLabel.label.grid(
                    row=1, column=1, columnspan=numberofsets-1) 
        
        butStart = tk.Button(self.frame, text="break", 
                    command = lambda:sequence( 
                        ssbreakLabel.start(), self.incrementCounter( numberofsets  ) 
                        )  
                    )   
        butStart.grid(row=1, column=0)

        butDone = tk.Button(self.frame, text="Superset Done", 
                command =  lambda:sequence (
                   self.destroy_frame(),
                   self.repInstance( self.setcount, t),
                    )
                )

        butDone.grid(row=1, column=numberofsets+1)

    def destroy_frame(self):
        if (self.count != 0):
            self.setcount += 1

        if (self.setcount  == len( self.superset) ):
            self.frame.quit()
        else:
            self.frame.destroy()

    def incrementCounter(self, limit):
        self.count+=1
        if (self.count == limit):
            self.count = 0
            self.setcount += 1
    
    def callGOWidget(self):
        self.GO = tk.Button(self.frame)
        self.GO["text"] = "GO"
        self.GO["command"] =  self.toObject
        self.GO.grid(row=0, column=0, padx=20)

################################
#   M A I N
################################
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r","--routine", help="routine name")

    args = parser.parse_args()

    root = tk.Tk()
#     root.title(args.routine)
    app = woToObject(args.routine, root)
    start = time.time()
    root.mainloop()
    end = time.time()
    root.destroy()
    
    out_file = open("workout.log", 'a')
    out_file.write( 
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\t" 
            + args.routine + "\t" 
            + str(end-start) + "\n" )
    out_file.close()
 
if __name__ == "__main__":
    main()

