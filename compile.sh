gcc -DRUN_VORONOI \
	src/math/compiled/distance.c \
	src/math/compiled/vector2.c \
	src/math/compiled/voronoi.c \
	src/o10n/compiled/bitmatrix.c \
	src/math/compiled/matrix.c \
	src/math/compiled/voronoi_run.c \
	-o bin/voronoi_run.so \
	-pg

gcc -shared -fPIC -o bin/compiled.so \
	src/math/compiled/distance.c \
	src/math/compiled/vector2.c \
	src/o10n/compiled/bitmatrix.c \
	src/math/compiled/matrix.c \
	src/math/compiled/voronoi.c 
