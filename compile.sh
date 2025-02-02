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
	src/math/compiled/voronoi.c \
	src/world/compiled/biome.c \
	src/world/compiled/water_distance.c

gcc -DTEST_WATER_DISTANCE \
	src/math/compiled/matrix.c \
	src/world/compiled/water_distance.c \
	src/world/compiled/test_water_distance.c \
	-o bin/test_water_distance.so \
	-pg

gcc -DTEST_BIOME \
	src/math/compiled/matrix.c \
	src/world/compiled/water_distance.c \
	src/world/compiled/biome.c \
	src/world/compiled/test_biome.c \
	-o bin/test_biome.so \
	-pg
