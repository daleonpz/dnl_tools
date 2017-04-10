#!/usr/bin/python2.7
###############################
#  T O   D O
###############################
# Add stats
# Improve GUI

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
        self.superset = [x for x in self.superset if x not in ('\n','')]
    
        self.frame = tk.Frame(master)
        self.frame.grid()
        self.callGOWidget()

    def toObject(self):
        self.frame.destroy()
        struct = []
        self.sslen = len(self.superset)
        self.count = 0
        self.ssetcount = 1
        
        self.repInstance(False) 
            

    def repInstance(self, addSSetCounter):
        if addSSetCounter: self.ssetcount += 1
        if self.ssetcount > self.sslen: 
            self.frame.quit()  
            return None

        self.frame = tk.Frame(self.master) # new frame
        self.frame.grid()

            # sets of this superset
        sets =  re.split("\n\* ",self.superset[ self.ssetcount - 1 ])
        ssrep = re.findall("[0-9:]+", sets[0] ) # superset rep
            #  [ rep , break] , check this part, later ;)
        rset = [ re.split("\n",x) for x in sets[1:] ]# set reps
            #  [ ex , rep, break ]

        numberofsets = int(ssrep[0])
        
        tk.Label(self.frame , 
                text = " ----------------------------- \n S U P E R S E T   " + 
                        str(self.ssetcount) + "/" + str(self.sslen) + 
                        " \n ----------------------------- ",
                font=('Helvetica',15,"bold")
                ).grid(
                    row=0, column=0, columnspan=numberofsets  
                    )

#         ssbreakLabel = Countdown(ssrep[1], self.frame)
        ssbreakLabel = Countdown("00:02", self.frame)
            # possible bug, when ssrep[0] = 0
        ssbreakLabel.label.grid(
                    row=1, column=1, columnspan=numberofsets-1) 

             # rset = [  [ ex , rep, break ]...]
        numberofexcercises = len(rset)        
        
        butStart = tk.Button(self.frame, text="Set Break", font=("fixedsys",10,"bold"), 
                    command = lambda:sequence( 
                        ssbreakLabel.start(), 
                        self.incrementCounter( numberofsets+1 ),
                        self.updateLabels(numberofexcercises, numberofsets, rset)
                        )  
                    )   
        butStart.grid(row=1, column=0)

        self.updateLabels(numberofexcercises, numberofsets, rset)

        butDone = tk.Button(self.frame, text="Superset Done", font=("fixedsys",10,"bold"),
                borderwidth=5,
                command =  lambda:sequence (
                   self.destroy_frame(),
                   self.repInstance(True),
                    )
                )

        butDone.grid(row=numberofexcercises+2, column=0)


    def destroy_frame(self):
        if (self.ssetcount  == len( self.superset) ):
            self.frame.quit()
        else:
            self.frame.destroy()
            self.count = 0

    def incrementCounter(self, limit):
        self.count+=1
        if (self.count == limit):
            self.count = 0
            self.destroy_frame()
            self.repInstance( True )
   
    def updateLabels(self, numberofexcercises, numberofsets, rset):
            for j in range(numberofexcercises):
                excercise = rset[j]
                tk.Label(self.frame, text = excercise[0],font=("fixedsys",15)).grid(
                            row = 2+j, column=0)
     
                for k in range(numberofsets):
                    if k == self.count:
                        bg = "red"
                    else:
                        bg = "white"

                    if ( len(excercise) != 2 ):
                       label = tk.Label(self.frame, text = "\n".join(excercise[1:]),
                               font=("fixedsys",15) )
                    else:
                       label = tk.Label(self.frame, text = excercise[1], 
                           font=("fixedsys",15) )

                    label.configure(bg=bg)
                    label.grid( row = 2+j, column=1+k, padx=5, pady=4)
 
    def callGOWidget(self):
        self.GO = tk.Button(self.frame)
        self.GO["text"] = "GO"
        self.GO["command"] =  self.toObject
        self.GO["font"] = ("fixedsys",50,"bold")
        self.GO["borderwidth"] = 10
        self.GO.grid(row=0, column=0, padx=20)

################################
#   M A I N
################################
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r","--routine", help="routine name")

    args = parser.parse_args()

    root = tk.Tk()
    root.title("Workout of the day")
#     root.geometry("400x250")
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

