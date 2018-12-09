import sys, os

samples = open(os.path.expanduser(sys.argv[1]), "r").readlines()
samples_to_go = len(samples)
files = 0

if not os.path.exists("julia_scripts"):
    os.makedirs("julia_scripts")

while (samples_to_go > 0):
    file = open("cohort" + str(files) + ".sh", "w")
    file.write("#!/bin/bash\n")
    file.write("#SBATCH -t 7- #days\n")
    files += 1

    for i in range(min(samples_to_go, int(sys.argv[2]))):
        file.write("julia julia_scripts/cohort" + str(len(samples) - samples_to_go) + ".jl\n")
        jfile = open("cohort" + str(len(samples) - samples_to_go) + ".jl", "w")
        jfile.write("using SubClonalSelection\n")
        jfile.write("l = fitABCmodels(\"cohort_samples/" + samples[len(samples) - samples_to_go][:-1] + ".txt\",\n")
        jfile.write("  \"" + samples[len(samples) - samples_to_go][:-1] + "\",\n")
        jfile.write("  read_depth = 300,\n")
        jfile.write("  Nmaxinf = 10^6,\n")
        jfile.write("  maxiterations = 5*10^5,\n")
        jfile.write("  resultsdirectory = \"results_cohort\",\n")
        jfile.write("  save = true,\n")
        jfile.write("  verbose = true,\n")
        jfile.write("  nparticles = 400);\n")
        jfile.write("l\n")
        jfile.write("saveresults(l, resultsdirectory = \"results_cohort\")\n")
        if (len(sys.argv) > 2 and sys.argv[3] == "-g"):
            jfile.write("plotmodelposterior(l)\n")
            jfile.write("plothistogram(l, 0)\n")
            jfile.write("plothistogram(l, 1)\n")
            jfile.write("plothistogram(l, 2)\n")
            jfile.write("plotparameterposterior(l, 0)\n")
            jfile.write("plotparameterposterior(l, 1)\n")
            jfile.write("plotparameterposterior(l, 2)\n")
            jfile.write("saveallplots(l, resultsdirectory = \"results_cohort\")\n")
        jfile.close()
        samples_to_go -= 1
    file.close()
