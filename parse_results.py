import os, sys
import matplotlib.pyplot as plt
import scipy.stats as st
import pandas as pd

def ks_tests(stat, data, comparisons, file):
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            test_res = ""
            test_res += "KS-Testing " + stat + " for " + comparisons[i] + " and " + comparisons[j] + ":\n"
            res = st.ks_2samp(data[i], data[j])
            test_res += "KS statistic: " + str(res[0]) + "\n"
            test_res += "p-value: " + str(res[1]) + "\n"
            if res[1] < 0.05:
                test_res += "Significant at the 0.05 level\n"
            else:
                test_res += "Insignificant at the 0.05 level\n"
            file.write(test_res + "\n")


def regressions(coeffs, cell, file):
    for i in range(len(coeffs)):
        test_res = ""
        test_res += "Regressing μ/β coefficient and cellularity for " + str(i) + "-subclone model:\n"
        res = st.linregress(coeffs[i], cell[i])
        test_res += "Slope: " + str(res[0]) + "\n"
        test_res += "Intercept: " + str(res[1]) + "\n"
        test_res += "r-value: " + str(res[2]) + "\n"
        test_res += "p-value: " + str(res[3]) + "\n"
        test_res += "stderr: " + str(res[4]) + "\n"
        if res[3] < 0.05:
            test_res += "Significant at the 0.05 level\n"
        else:
            test_res += "Insignificant at the 0.05 level\n"
        file.write(test_res + "\n")


def cell_coeff(sub_0, sub_1, sub_2, test_results):
    # Cellularity vs μ/β
    fig = plt.figure()
    a = plt.scatter(x=sub_0[0], y=sub_0[1], color="red")
    b = plt.scatter(x=sub_1[0], y=sub_1[2], color="green")
    c = plt.scatter(x=sub_2[0], y=sub_2[3], color="blue")
    plt.legend((a, b, c), ("0-subclone", "1-subclone", "2-subclone"))
    plt.title("Full μ/β and Cellularity Model")
    plt.xlabel("μ/β Coefficients")
    plt.ylabel("Cellularity")
    fig.savefig("sub_plot.png")

    # Regressions
    coeffs = [sub_0[0], sub_1[0], sub_2[0]]
    cell = [sub_0[1], sub_1[2], sub_2[3]]
    regressions(coeffs, cell, test_results)


def coeff_box(sub_0, sub_1, sub_2, test_results):
    # μ/β
    plt.figure()
    plt.title("μ/β Boxplot Comparison")
    plt.ylabel("μ/β Coefficients")
    plt.tick_params(
        axis='x',
        which='both',
        bottom=False,
        top=False)
    plt.boxplot([sub_0[0], sub_1[0], sub_2[0], sub_0[0] + sub_1[0] + sub_2[0]],
                labels=["0-subclone", "1-subclone", "2-subclone", "all models"], showfliers=False)
    plt.savefig("sub_coeffs")

    # Tests
    comparisons = ["0-subclone", "1-subclone", "2-subclone"]
    data = [sub_0[0], sub_1[0], sub_2[0]]
    ks_tests("μ/β coefficient", data, comparisons, test_results)


def fit_box(sub_1, sub_2, test_results):
    # Fitness
    plt.figure()
    plt.title("Subclone Fitness Boxplot Comparison")
    plt.tick_params(
        axis='x',
        which='both',
        bottom=False,
        top=False)
    plt.ylabel("Subclone Fitness")
    plt.boxplot([sub_1[1], sub_2[1], sub_2[2], sub_2[1] + sub_2[2], sub_1[1] + sub_2[1] + sub_2[2]],
                labels=["1-subclone", "2-sub 1st", "2-sub 2nd", "2-sub all", "all models"],
                showfliers=False)
    plt.savefig("sub_fitness")

    # Tests
    comparisons = ["1-subclone", "2-subclone 1st sample", "2-subclone 2nd sample"]
    data = [sub_1[1], sub_2[1], sub_2[2]]
    ks_tests("Subclone Fitness", data, comparisons, test_results)


def cell_box(sub_0, sub_1, sub_2, test_results):
    # Cellularity
    plt.figure()
    plt.title("Subclone Cellularity Boxplot Comparison")
    plt.tick_params(
        axis='x',
        which='both',
        bottom=False,
        top=False)
    plt.ylabel("Subclone Cellularity")
    plt.boxplot([sub_0[1], sub_1[2], sub_2[3], sub_0[1] + sub_1[2] + sub_2[3]],
                labels=["0-subclone", "1-subclone", "2-subclone", "all models"], showfliers=False)
    plt.savefig("sub_cell")

    # Tests
    comparisons = ["0-subclone", "1-subclone", "2-subclone"]
    data = [sub_0[1], sub_1[2], sub_2[3]]
    ks_tests("Celluarity", data, comparisons, test_results)

def parse_text(data, sub_0, sub_1, sub_2, file):
    important_results = ["Parameter 1 - μ/β: ",
                         "Parameter 3 - Cellularity: ",
                         "Parameter 3 - Fitness: ",
                         "Parameter 5 - Cellularity: ",
                         "Parameter 3 - Fitness - Subclone 1: ",
                         "Parameter 5 - Fitness - Subclone 2: ",
                         "Parameter 7 - Cellularity: "]

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

def separate_results(file):
    data_list = [line.strip() for line in file.readlines()]
    important_results = [
        "Parameter 1 - μ/β: ",
        "Parameter 2 - Clonal Mutations: ",
        "Parameter 3 - Cellularity: ",
        "Parameter 3 - Fitness: ",
        "Parameter 4 - Time (tumour doublings): ",
        "Parameter 5 - Cellularity: ",
        "Parameter 6 - Subclone Frequency: ",
        "Parameter 7 - Subclone Mutations: ",
        "Parameter 3 - Fitness - Subclone 1: ",
        "Parameter 4 - Time (tumour doublings) - Subclone 1: ",
        "Parameter 5 - Fitness - Subclone 2: ",
        "Parameter 6 - Time (tumour doublings) - Subclone 2: ",
        "Parameter 7 - Cellularity: ",
        "Parameter 8 - Subclone 1 Frequency: ",
        "Parameter 9 - Subclone 2 Frequency: ",
        "Parameter 10 - Subclone 1 Mutations: ",
        "Parameter 11 - Subclone 2 Mutations: ",
    ]
    important_lengths = [len(x) for x in important_results]
    cats = [
        "Model 1 μ/β",
        "Model 1 Clonal Mutations",
        "Model 1 Cellularity",
        "Model 2 μ/β",
        "Model 2 Clonal Mutations",
        "Model 2 Fitness",
        "Model 2 Time",
        "Model 2 Cellularity",
        "Model 2 Subclone Frequency",
        "Model 2 Subclone Mutations",
        "Model 3 μ/β",
        "Model 3 Clonal Mutations",
        "Model 3 Fitness Subclone 1",
        "Model 3 Time Subclone 1",
        "Model 3 Fitness Subclone 2",
        "Model 3 Time Subclone 2",
        "Model 3 Cellularity",
        "Model 3 Subclone 1 Frequency",
        "Model 3 Subclone 2 Frequency",
        "Model 3 Subclone 1 Mutations",
        "Model 3 Subclone 2 Mutations",
    ]
    cols = []
    for i in cats:
        cols.append(i)
        cols.append(i + " Interval")

    df = pd.DataFrame(columns=cols)
    res = []
    res_dict = {}
    for line in data_list:
        for i in range(len(important_results)):
            if len(line) > important_lengths[i] and line[:important_lengths[i]] == important_results[i]:
                text = line[important_lengths[i]:]
                res.append(text[:text.index("(")])
                res.append(text[text.index("("):])
            elif line == "" or line == "\n":
                if len(res) == 36:
                    res = ["", "", "", "", "", ""] + res

                if len(res) == 42:
                    for j in range(42):
                        res_dict[cols[j]] = res[j]
                    df = df.append(res_dict, ignore_index=True)

                res = []
                res_dict = {}

    df.to_csv("results.csv")


if __name__ == "__main__":
    directory = sys.argv[1]
    file = open("results.txt", "w", encoding="utf-8")
    sub_0 = [[], []]  # μ/β, Cellularity
    sub_1 = [[], [], []]  # μ/β, Fitness, Cellularity
    sub_2 = [[], [], [], []]  # μ/β, Fitness 1, Fitness 2, Cellularity

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        data = open(file_path, "r", encoding="utf-8")
        parse_text(data, sub_0, sub_1, sub_2, file)
    file.close()

    file = open("results.txt", "r", encoding="utf-8")
    separate_results(file)
    file.close()

    test_results = open("stat_results.txt", "w", encoding="utf-8")
    cell_coeff(sub_0, sub_1, sub_2, test_results)
    coeff_box(sub_0, sub_1, sub_2, test_results)
    fit_box(sub_1, sub_2, test_results)
    cell_box(sub_0, sub_1, sub_2, test_results)

    test_results.close()
