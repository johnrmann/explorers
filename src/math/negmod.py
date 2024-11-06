def negmod(x, modulo):
	if x < 0:
		return -x % modulo
	return x % modulo
