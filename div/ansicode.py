print("\033[s", "123"*100, "\033[u", "Overwrite", sep='')
print("\033[%dA" % 3, "Overwrite", sep='')