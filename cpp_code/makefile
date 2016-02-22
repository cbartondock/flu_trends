CC = g++
LDFLAGS = 
CFLAGS = -c -Wall

%.o: %.cpp ${includes}
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS)

clean:
	rm *.o
