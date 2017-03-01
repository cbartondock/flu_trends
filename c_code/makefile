all: dylibs/useful_functions.dylib dylibs/outbreak_sim.dylib dylibs/dynamic_array.dylib dylibs/hash_table.dylib dylibs/mersenne_twister.dylib
exe: outbreak_sim

dylibs/%.dylib : %.c
	/usr/bin/gcc -O3 -std=c99 -Wall -lm -dynamiclib -o $@ $^
clean:
	rm -rf *.so *.o dylibs/*.dylib; rm -f outbreak_sim
