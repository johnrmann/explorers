import pstats

p = pstats.Stats('prof.prof')
p.sort_stats('cumulative').print_stats(100)
