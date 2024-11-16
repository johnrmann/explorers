gcc -DRUN_VORONOI -o bin/voronoi_run.so \
	src/math/compiled/distance.c \
	src/math/compiled/vector2.c \
	src/math/compiled/voronoi.c \
	src/math/compiled/voronoi_run.c

gcc -shared -fPIC -o bin/compiled.so \
	src/math/compiled/distance.c \
	src/math/compiled/vector2.c \
	src/math/compiled/voronoi.c 
