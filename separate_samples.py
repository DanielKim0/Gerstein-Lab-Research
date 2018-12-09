import sys, os

file = open(os.path.expanduser(sys.argv[1]), "r")
for line in file.readlines():
    curr_file_s = ""
    if (line[0] != '\t'):
        line_split = line.split()
        if curr_file_s != line_split[0]:
            curr_file_s = line_split[0]
            curr_file = open(curr_file_s + ".txt", "a+")
            # print(curr_file_s)
        curr_file.write(str(line_split[-1]) + "\n")
