CC=g++

# optimizations
OPT_1= -Wall -Wextra 

OPTIONS= $(OPT_1) -O0 -g 

CFLAGS= $(OPTIONS) 

LIB=-lpq

#-------------------------------------------------------
OBJ=  imdbinterface.o
TARGET= test

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $(TARGET)  $(OBJ) $(LIB)


#-------------------------------------------------------
clean:
	rm -rf *~
	rm -rf $(OBJ)
	rm -rf $(TARGET)


