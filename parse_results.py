import os, sys
import matplotlib.pyplot as plt

file = open("results.txt", "w")
sub_0 = [[], []]  # μ/β, Cellularity
sub_1 = [[], [], []]  # μ/β, Fitness, Cellularity
sub_2 = [[], [], [], []]  # μ/β, Fitness 1, Fitness 2, Cellularity
important_results = ["Parameter 1 - Î¼/Î²: ",
                     "Parameter 3 - Cellularity: ",
                     "Parameter 3 - Fitness: ",
                     "Parameter 5 - Cellularity: ",
                     "Parameter 3 - Fitness - Subclone 1: ",
                     "Parameter 5 - Fitness - Subclone 2: ",
                     "Parameter 7 - Cellularity: "]
files = 0

for filename in os.listdir(os.path.expanduser(sys.argv[1])):
    file_path = os.path.join(os.path.expanduser(sys.argv[1]), filename)
    data = open(file_path, "r")
    data_list = [line.strip() for line in data.readlines()]
    curr_pop = ""
    prev_pop = ""
    results = []
    prev_results = []

    in_results = False
    for line in data_list:
        relevant = 0

        if line == "########################################":
            in_results = True
        elif len(line) > 0 and (line[0] == "W" or line[:3] == "New"):
            if in_results:
                curr_pop = prev_pop
                results = prev_results
                file.write(curr_pop + "\n")
                files += 1

                if len(results) == 7:
                    for i in range(3):
                        sub_1[i].append(results[i])
                    for i in range(4):
                        sub_2[i].append(results[i + 3])
                elif len(results) == 9:
                    for i in range(2):
                        sub_0[i].append(results[i])
                    for i in range(3):
                        sub_1[i].append(results[i + 2])
                    for i in range(4):
                        sub_2[i].append(results[i + 5])
            curr_pop = ""
            prev_pop = ""
            results = []
            prev_results = []
            in_results = False
        elif in_results:
            if len(line) > 0 and line[0:2] == "Po":
                prev_pop = curr_pop
                prev_results = results
                curr_pop = ""
                results = []

            if len(line) > 0:
                for imp in important_results:
                    if (len(line) > len(imp) and line[:len(imp)] == imp):
                        relevant = len(imp)
                        break

                if relevant > 0:
                    results.append(float(line[relevant:relevant + 4]))
                curr_pop += line + "\n"

    if len(curr_pop) > 0:
        file.write(curr_pop + "\n")
        files += 1

        if len(results) == 7:
            for i in range(3):
                sub_1[i].append(results[i])
            for i in range(4):
                sub_2[i].append(results[i + 3])
        elif len(results) == 9:
            for i in range(2):
                sub_0[i].append(results[i])
            for i in range(3):
                sub_1[i].append(results[i + 2])
            for i in range(4):
                sub_2[i].append(results[i + 5])

        data.close()

    files = 0

# μ/β
plt.boxplot(sub_0[0])
plt.savefig("sub_0_coeffs")
plt.boxplot(sub_1[0])
plt.savefig("sub_1_coeffs")
plt.boxplot(sub_2[0])
plt.savefig("sub_2_coeffs")
plt.boxplot(sub_0[0] + sub_1[0] + sub_2[0])
plt.savefig("sub_all_coeffs")

# Fitness
plt.boxplot(sub_1[1])
plt.savefig("sub_1_fitness")
plt.boxplot(sub_2[1])
plt.savefig("sub_2_1_fitness")
plt.boxplot(sub_2[2])
plt.savefig("sub_2_2_fitness")
plt.boxplot(sub_2[1] + sub_2[2])
plt.savefig("sub_2_comb_fitness")
plt.boxplot(sub_1[1] + sub_2[1] + sub_2[2])
plt.savefig("sub_all_fitness")

# Cellularity
plt.boxplot(sub_0[1])
plt.savefig("sub_0_cell")
plt.boxplot(sub_1[2])
plt.savefig("sub_1_cell")
plt.boxplot(sub_2[3])
plt.savefig("sub_2_cell")
plt.boxplot(sub_0[1] + sub_1[2] + sub_2[3])
plt.savefig("sub_all_cell")

# Cellularity vs μ/β
plt.plot(x=sub_0[0], y=sub_0[1])
plt.savefig("sub_0_plot")
plt.plot(x=sub_1[0], y=sub_1[2])
plt.savefig("sub_1_plot")
plt.plot(x=sub_2[0], y=sub_2[3])
plt.savefig("sub_2_plot")
plt.plot(x=sub_0[0] + sub_1[0] + sub_2[0], y=sub_0[1] + sub_1[2] + sub_2[3])
plt.savefig("sub_all_plot")

file.close()