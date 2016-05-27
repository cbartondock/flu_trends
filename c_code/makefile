all: dylibs/outbreak_sim.dylib dylibs/dynamic_array.dylib
exe: outbreak_sim

dylibs/%.dylib : %.c
	gcc-4.8 -O3 -std=c99 -Wall -lm -dynamiclib -o $@ $^
clean:
	rm -rf *.so *.o dylibs/*.dylib; rm -f outbreak_sim
