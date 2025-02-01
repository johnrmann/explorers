import pstats

p = pstats.Stats('prof.prof')
p.sort_stats('tottime').print_stats(100)
