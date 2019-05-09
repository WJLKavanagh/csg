l = ['K_K', 'K_A', 'K_W', 'A_K', 'A_A', 'A_W', 'A_KA', 'A_KW', 'A_AW', 'W_K', 'W_A', 'W_W']

for single_t in l:
  single_a = 13                                       # the value for 'attack' is
  if single_t[0] == "A": single_a += 3                # silly numerisation...
  if single_t[0] == "W": single_a += 9
  if single_t[2] == "A": single_a += 1
  if single_t[2] == "W": single_a += 2
  if len(single_t) > 3 and "KA" in single_t: single_a += 3
  elif len(single_t) > 3: single_a += 4
  print(single_t, single_a)
