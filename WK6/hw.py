
uncompressed=lambda s:''.join(map(lambda t:t[0]*int(t[1]),zip(list(s)[1::2],list(s)[::2])))

print uncompressed('2a5b1c')
