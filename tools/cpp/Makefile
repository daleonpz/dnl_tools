CC=g++

OPT_1= -Wall -Wextra 
OPTIONS= $(OPT_1) -O0 -g 
CFLAGS= $(OPTIONS) 
LIB=-lpq
DEPS=parse.cc db_interface.cc

#-------------------------------------------------------
OBJ=  imdbinterface.o
TARGET= test

$(TARGET): $(OBJ)  
	$(CC) $(CFLAGS) -o $(TARGET)  $(OBJ) $(DEPS) $(LIB) 


#-------------------------------------------------------
clean:
	rm -rf *~
	rm -rf $(OBJ)
	rm -rf $(TARGET)


