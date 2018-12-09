import os, sys, random
data = open(os.path.expanduser(sys.argv[1]), "r")

data_list = data.readlines()
data_list = [line.strip() for line in data_list]

if not os.path.exists("data"):
    os.makedirs("data")

data_list_len = len(data_list)
for num in [4, 8, 16, 32, 64]:
    file = open("data/data_" + str(num) + ".txt", "w")
    for item in random.sample(int(data_list_len / num)):
        file.write(item)
    file.close()

if not os.path.exists("bash_scripts"):
    os.makedirs("bash_scripts")

file_names = ["1000k_iter", "100k_iter", "250k_iter", "500k_iter", "data_4", "data_8", "data_16", "data_32", "data_64"]
for ind in range(len(file_names)):
    my_dir = os.path.expanduser("/bash_scripts/" + file_names[ind] + ".sh")
    file = open(my_dir, "w")
    file.write("#!/bin/bash\n")
    file.write("#SBATCH -t 7- #days\n")
    file.write("julia julia_scripts/" + file_names[ind] + ".jl\n")

if not os.path.exists("julia_scripts"):
    os.makedirs("julia_scripts")

for name in file_names:
    my_dir = os.path.expanduser("/julia_scripts/" + name + ".jl")
    file = open(my_dir, "w")
    file.write("using SubClonalSelection\n")
    if (name[-1] == "r"):
        file.write("l = fitABCmodels(\"data/data_8.txt\",\n")
    else:
        file.write("l = fitABCmodels(\"data/" + name + ".txt\",\n")
    file.write("  \"" + name + "\",\n")
    file.write("  read_depth = 300,\n")
    file.write("  Nmaxinf = 10^6,\n")
    if (name == "1000k_iter"):
        file.write("  maxiterations = 10^6,\n")
    elif (name == "250k_iter"):
        file.write("  maxiterations = 2.5*10^5,\n")
    elif (name == "100k_iter"):
        file.write("  maxiterations = 1*10^5,\n")
    else:
        file.write("  maxiterations = 5*10^5,\n")
    file.write("  resultsdirectory = \"results\",\n")
    file.write("  save = true,\n")
    file.write("  verbose = true,\n")
    file.write("  nparticles = 400);\n")
    file.write("l\n")
    file.write("saveresults(l, resultsdirectory = \"/results\")\n")
    if (len(sys.argv) > 2 and sys.argv[3] == "-g"):
        file.write("plotmodelposterior(l)\n")
        file.write("plothistogram(l, 0)\n")
        file.write("plothistogram(l, 1)\n")
        file.write("plothistogram(l, 2)\n")
        file.write("plotparameterposterior(l, 0)\n")
        file.write("plotparameterposterior(l, 1)\n")
        file.write("plotparameterposterior(l, 2)\n")
        file.write("saveallplots(l, resultsdirectory = \"/results\")\n")
    file.close()
