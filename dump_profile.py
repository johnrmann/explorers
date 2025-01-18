import pstats

p = pstats.Stats('prof.prof')
p.sort_stats('cumtime').print_stats(100)
