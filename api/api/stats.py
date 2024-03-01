import pstats

p = pstats.Stats('profile.prof')
p.sort_stats('cumulative').print_stats(10)