all: dylibs/outbreak_sim.dylib
exe: outbreak_sim

dylibs/%.dylib : %.c
	/usr/local/bin/gcc-5 -O3 -std=c99 -Wall -fopenmp -lm -dynamiclib -o $@ $^
clean:
	rm -rf *.so *.o dylibs/*.dylib
