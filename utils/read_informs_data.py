#!/usr/bin/env python
# coding=utf-8

# Read data and read tree fuctions for INFORMS data
# user att ['DUID','PID','DUPERSID','DOBMM','DOBYY','SEX','RACEX','RACEAX','RACEBX','RACEWX','RACETHNX','HISPANX','HISPCAT','EDUCYEAR','Year','marry','income','poverty']
# condition att ['DUID','DUPERSID','ICD9CODX','year']
from models.gentree import GenTree
import pickle, pdb
from models.numrange import NumRange
from utils.utility import cmp_str

__DEBUG = False
ATT_NAMES = ['DUID', 'PID', 'DUPERSID', 'DOBMM', 'DOBYY', 'SEX', 'RACEX', 'RACEAX', 'RACEBX', 'RACEWX', 'RACETHNX', 'HISPANX', 'HISPCAT', 'EDUCYEAR', 'Year', 'marry', 'income', 'poverty']
QI_INDEX = [3, 4, 6, 13, 15, 16]
# if you want to achieve better utility, you can set some numeric attribute
# to be False. Then the program will treat it as a numeric attributes
# and generate range values without generalization hierarchy
IS_CAT = [False, False, False, False, False, False]
SA_index = -1

def read_tree(flag=0):
    """read tree from data/tree_*.txt, store them in att_tree
    """
    att_names = []
    att_trees = []
    for t in QI_INDEX:
        att_names.append(ATT_NAMES[t])
    for i in range(len(att_names)):
        if IS_CAT[i]:
            att_trees.append(read_tree_file(att_names[i]))
        else:
            att_trees.append(read_pickle_file(att_names[i]))
    return att_trees


def read_pickle_file(att_name):
    """
    read pickle file for numeric attributes
    return numrange object
    """
    with open('data/informs_' + att_name + '_static.pickle', 'rb') as static_file:
        (numeric_dict, sort_value) = pickle.load(static_file)
        result = NumRange(sort_value, numeric_dict)
        return result


def read_tree_file(treename):
    """read tree data from treename
    """
    leaf_to_path = {}
    att_tree = {}
    prefix = 'data/informs_'
    postfix = ".txt"
    treefile = open(prefix + treename + postfix, 'rU')
    att_tree['*'] = GenTree('*')
    if __DEBUG:
        print "Reading Tree" + treename
    for line in treefile:
        # delete \n
        if len(line) <= 1:
            break
        line = line.strip()
        temp = line.split(';')
        # copy temp
        temp.reverse()
        for i, t in enumerate(temp):
            isleaf = False
            if i == len(temp) - 1:
                isleaf = True
            if t not in att_tree:
                # always satisfy
                att_tree[t] = GenTree(t, att_tree[temp[i - 1]], isleaf)
    if __DEBUG:
        print "Nodes No. = %d" % att_tree['*'].support
    treefile.close()
    return att_tree


def read_data(flag=0):
    """read microda for *.txt and return read data
    """
    """read microdata for *.txt and return read data"""
    QI_num = len(QI_INDEX)
    data = []
    numeric_dict = []
    for i in range(QI_num):
        numeric_dict.append(dict())
    data_file = open('data/demographics.csv', 'rU')
    for line in data_file:
        line = line.strip()
        # remove empty
        if len(line) == 0:
            continue
        # remove double spaces
        line = line.replace(' ', '')
        temp = line.split(',')
        ltemp = []
        for i in range(QI_num):
            index = QI_INDEX[i]
            if IS_CAT[i] is False:
                try:
                    numeric_dict[i][temp[index]] += 1
                except KeyError:
                    numeric_dict[i][temp[index]] = 1
            ltemp.append(temp[index])
        ltemp.append(temp[SA_index])
        data.append(ltemp)
    # pickle numeric attributes and get NumRange
    for i in range(QI_num):
        if IS_CAT[i] is False:
            static_file = open('data/informs_' + ATT_NAMES[QI_INDEX[i]] + '_static.pickle', 'wb')
            sort_value = list(numeric_dict[i].keys())
            sort_value.sort(cmp=cmp_str)
            pickle.dump((numeric_dict[i], sort_value), static_file)
            static_file.close()
    return data