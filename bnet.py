import sys
import pandas as pd

def return_learned_probs(training_data):
    alphabets = ["B", "G", "C", "F"]
    df = pd.read_csv(training_data, sep=" ", names=alphabets)
    length = len(df)
    prob_of_b = df["B"].value_counts() / length
    prob_of_gb = df.groupby(["G", "B"])["B"].count() / df.groupby("B")["B"].count()
    prob_of_fgc = df.groupby(["F", "G", "C"])["F"].count() / df.groupby(["G", "C"])["F"].count()
    prob_of_c = df["C"].value_counts() / length
    return prob_of_b, prob_of_gb, prob_of_fgc, prob_of_c

def print_learned_probs(prob_of_b, prob_of_gb, prob_of_fgc, prob_of_c):
    print("Table of P(B):")
    for b, prob in prob_of_b.items():
        print("P(B={}) = {}".format(b, prob))
    print("\nTable of P(G|B):")
    for (g, b), prob in prob_of_gb.items():
        print("P(G={} | B={}) = {}".format(g, b, prob))
    print("\nTable of P(F|G,C):")
    for (g, c, f), prob in prob_of_fgc.items():
        print("P(F={} | G={}, C={}) = {}".format(f, g, c, prob))
    print("\nTable of P(C):")
    for c, prob in prob_of_c.items():
        print("P(C={}) = {}".format(c, prob))

def return_jpd_value(prob_of_b, prob_of_gb, prob_of_fgc, prob_of_c, value_of_b_alpha, value_of_g_alpha, value_of_c_alpha, value_of_f_alpha):
    b_value = prob_of_b[value_of_b_alpha]
    gb_value = prob_of_gb[value_of_g_alpha][value_of_b_alpha]
    fgc_value = prob_of_fgc[value_of_g_alpha][value_of_c_alpha][value_of_f_alpha]
    c_value = prob_of_c[value_of_c_alpha]
    jpd_result = b_value*gb_value*fgc_value*c_value
    return jpd_result

if len(sys.argv)!=6:
    print("Wrong argument values")
else:
    training_data = sys.argv[1]
    value_of_b_alpha = 1 if sys.argv[2]=='Bt' else 0
    value_of_g_alpha = 1 if sys.argv[3]=='Gt' else 0
    value_of_c_alpha = 1 if sys.argv[4]=='Ct' else 0
    value_of_f_alpha = 1 if sys.argv[5]=='Ft' else 0
    prob_of_b, prob_of_gb, prob_of_fgc, prob_of_c = return_learned_probs(training_data)
    print_learned_probs(prob_of_b, prob_of_gb, prob_of_fgc, prob_of_c)
    jpd_result = return_jpd_value(prob_of_b, prob_of_gb, prob_of_fgc, prob_of_c, value_of_b_alpha, value_of_g_alpha, value_of_c_alpha, value_of_f_alpha)
    print("\nJPD Result:")
    print("P(B= {}, G= {}, C= {}, F= {}) = {}".format(value_of_b_alpha, value_of_g_alpha, value_of_c_alpha, value_of_f_alpha, jpd_result))