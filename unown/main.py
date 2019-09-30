# baca data dari unown.bin
with open("unown.bin", 'rb') as infile:
    data = infile.read()

# ubah data ke str
data = "".join([str(int(d)) for d in data])

# append satu char 0 ke data
data += "0"

# split per 7 binary dan convert ke char
data = ["".join(chr(int(data[i:i+7], 2))) for i in range(0, len(data), 7)]

# print data yang direverse
print("".join(data[::-1]))
