

all: main.o video_selector.o
	gcc -g -Wall -W -o  main main.o video_selector.o -lavutil -lavformat -lavcodec -lswscale -lz -lm  `sdl-config --cflags --libs` 

main.o : main.c headers/video_selector.h
	gcc -g -Wall -W -c main.c headers/video_selector.h -lavutil -lavformat -lavcodec -lswscale -lz -lm  `sdl-config --cflags --libs` 

 
video_selector.o : headers/video_selector.c headers/video_selector.h 
	gcc -g -Wall -W -c headers/video_selector.c headers/video_selector.h  -lavutil -lavformat -lavcodec -lswscale -lz -lm  `sdl-config --cflags --libs` 

clean:
	rm -rf *~
	rm -rf *.o
	rm main

