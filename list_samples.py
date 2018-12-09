import sys, os

file = open(os.path.expanduser(sys.argv[1]), "r")
sample_set = set()
for line in file.readlines():
    if (line[0] != '\t'):
        line_split = line.split()
        if line_split[0] not in sample_set:
            sample_set.add(line_split[0])

file_1 = open("samples_enumerated.txt", "w")
file_2 = open("samples_listed.txt", "w")
num = 0
for sample in sorted(list(sample_set)):
    file_1.write(str(num) + "\t" + str(sample) + "\n")
    file_2.write(str(sample) + "\n")
    num += 1
