"""
run Basic_Mondrian with given parameters
"""

# !/usr/bin/env python
# coding=utf-8
from mondrian import mondrian_delete_missing
from mondrian import mondrian_split_missing
from mondrian import mondrian
from utils.read_data import read_data
from utils.read_data import read_tree
import sys, copy, random

# sys.setrecursionlimit(50000)

__DEBUG = True


def get_result_one(att_trees, data, k=10):
    "run mondrian for one time, with k=10"
    print "K=%d" % k
    print "Mondrian"
    data_back = copy.deepcopy(data)
    _, eval_result = mondrian(att_trees, data, k)
    print "NCP %0.2f" % eval_result[0] + "%"
    print "Running time %0.2f" % eval_result[1] + "seconds"
    print "Missing Pollution = %.2f %%" % eval_result[2]
    data = copy.deepcopy(data_back)
    _, eval_result = mondrian_delete_missing(att_trees, data, k)
    print "Mondrian Deletion"
    print "NCP %0.2f" % eval_result[0] + "%"
    print "Running time %0.2f" % eval_result[1] + "seconds"
    print "Missing Pollution = %.2f %%" % eval_result[2]


def get_result_k(att_trees, data):
    """
    change k, whle fixing QD and size of dataset
    """
    data_back = copy.deepcopy(data)
    all_ncp = []
    all_rtime = []
    all_pollution = []
    deletion_all_ncp = []
    deletion_all_rtime = []
    # for k in range(5, 105, 5):
    for k in [2, 5, 10, 25, 50, 100]:
        if __DEBUG:
            print '#' * 30
            print "K=%d" % k
            print "Mondrian"
        _, eval_result = mondrian(att_trees, data, k)
        data = copy.deepcopy(data_back)
        all_ncp.append(round(eval_result[0], 2))
        all_rtime.append(round(eval_result[1], 2))
        all_pollution.append(round(eval_result[2], 2))
        if __DEBUG:
            print "NCP %0.2f" % eval_result[0] + "%"
            print "Running time %0.2f" % eval_result[1] + "seconds"
            print "Missing Pollution = %.2f %%" % eval_result[2]
            print "Mondrian Deletion"
        _, eval_result = mondrian_delete_missing(att_trees, data, k)
        data = copy.deepcopy(data_back)
        if __DEBUG:
            print "NCP %0.2f" % eval_result[0] + "%"
            print "Running time %0.2f" % eval_result[1] + "seconds"
        deletion_all_ncp.append(round(eval_result[0], 2))
        deletion_all_rtime.append(round(eval_result[1], 2))
    print "Mondrian"
    print "All NCP", all_ncp
    print "All Running time", all_rtime
    print "Missing Pollution", all_pollution
    print "Mondrian Deletion"
    print "All NCP", deletion_all_ncp
    print "All Running time", deletion_all_rtime


def get_result_dataset(att_trees, data, k=10, n=10):
    """
    fix k and QI, while changing size of dataset
    n is the proportion nubmber.
    """
    data_back = copy.deepcopy(data)
    length = len(data_back)
    print "K=%d" % k
    joint = 5000
    datasets = []
    check_time = length / joint
    if length % joint == 0:
        check_time -= 1
    for i in range(check_time):
        datasets.append(joint * (i + 1))
    datasets.append(length)
    all_ncp = []
    all_rtime = []
    all_pollution = []
    deletion_all_ncp = []
    deletion_all_rtime = []
    for pos in datasets:
        ncp = rtime = pollution = 0
        if __DEBUG:
            print '#' * 30
            print "size of dataset %d" % pos
            print "Mondrian"
        for j in range(n):
            temp = random.sample(data, pos)
            result, eval_result = mondrian(att_trees, temp, k)
            ncp += eval_result[0]
            rtime += eval_result[1]
            pollution += eval_result[2]
            data = copy.deepcopy(data_back)
            # save_to_file((att_trees, temp, result, k, L))
        ncp /= n
        rtime /= n
        pollution /= n
        if __DEBUG:
            print "Average NCP %0.2f" % ncp + "%"
            print "Running time %0.2f" % rtime + "seconds"
            print "Missing Pollution = %.2f %%" % pollution + "%"
            print "Mondrian Deletion"
        all_ncp.append(round(ncp, 2))
        all_rtime.append(round(rtime, 2))
        all_pollution.append(round(eval_result[2], 2))
        ncp = rtime = 0
        for j in range(n):
            temp = random.sample(data, pos)
            result, eval_result = mondrian_delete_missing(att_trees, temp, k)
            ncp += eval_result[0]
            rtime += eval_result[1]
            data = copy.deepcopy(data_back)
            # save_to_file((att_trees, temp, result, k, L))
        ncp /= n
        rtime /= n
        if __DEBUG:
            print "Average NCP %0.2f" % ncp + "%"
            print "Running time %0.2f" % rtime + "seconds"
        deletion_all_ncp.append(round(ncp, 2))
        deletion_all_rtime.append(round(rtime, 2))
    print "Mondrian"
    print "All NCP", all_ncp
    print "All Running time", all_rtime
    print "Missing Pollution", all_pollution
    print "Mondrian Deletion"
    print "All NCP", deletion_all_ncp
    print "All Running time", deletion_all_rtime


def get_result_qi(att_trees, data, k=10):
    """
    change nubmber of QI, whle fixing k and size of dataset
    """
    data_back = copy.deepcopy(data)
    ls = len(data[0])
    all_ncp = []
    all_rtime = []
    all_pollution = []
    deletion_all_ncp = []
    deletion_all_rtime = []
    for i in reversed(range(1, ls)):
        if __DEBUG:
            print '#' * 30
            print "Number of QI=%d" % i
            print "Mondrian"
        _, eval_result = mondrian(att_trees, data, k, i)
        data = copy.deepcopy(data_back)
        if __DEBUG:
            print "NCP %0.2f" % eval_result[0] + "%"
            print "Running time %0.2f" % eval_result[1] + "seconds"
            print "Missing Pollution = %.2f %%" % eval_result[2] + "%"
            print "Mondrian Deletion"
        all_ncp.append(round(eval_result[0], 2))
        all_rtime.append(round(eval_result[1], 2))
        all_pollution.append(round(eval_result[2], 2))
        _, eval_result = mondrian_delete_missing(att_trees, data, k, i)
        data = copy.deepcopy(data_back)
        if __DEBUG:
            print "NCP %0.2f" % eval_result[0] + "%"
            print "Running time %0.2f" % eval_result[1] + "seconds"
            print "Mondrian Deletion"
        deletion_all_ncp.append(round(eval_result[0], 2))
        deletion_all_rtime.append(round(eval_result[1], 2))
    print "Mondrian"
    print "All NCP", all_ncp
    print "All Running time", all_rtime
    print "Missing Pollution", all_pollution
    print "Mondrian Deletion"
    print "All NCP", deletion_all_ncp
    print "All Running time", deletion_all_rtime


if __name__ == '__main__':
    FLAG = ''
    LEN_ARGV = len(sys.argv)
    try:
        FLAG = sys.argv[1]
    except:
        pass
    k = 10
    RAW_DATA = read_data()
    ATT_TREES = read_tree()
    # print '#' * 30
    if FLAG == 'k':
        get_result_k(ATT_TREES, RAW_DATA)
    elif FLAG == 'qi':
        get_result_qi(ATT_TREES, RAW_DATA)
    elif FLAG == 'data':
        get_result_dataset(ATT_TREES, RAW_DATA)
    elif FLAG == 'one':
        if LEN_ARGV > 3:
            k = int(sys.argv[3])
            get_result_one(ATT_TREES, RAW_DATA, k)
        else:
            get_result_one(ATT_TREES, RAW_DATA)
    elif FLAG == '':
        get_result_one(ATT_TREES, RAW_DATA)
    else:
        print "Usage: python anonymizer [a | i] [k | qi | data | one]"
        print "a: adult dataset, 'i': INFORMS ataset"
        print "K: varying k, qi: varying qi numbers, data: varying size of dataset, \
                one: run only once"
    # anonymized dataset is stored in result
    print "Finish Basic_Mondrian!!"
