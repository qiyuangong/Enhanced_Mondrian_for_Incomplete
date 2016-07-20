"""
utility functions
"""
# !/usr/bin/env python
# coding=utf-8


def cmp_str(element1, element2):
    """compare number in str format correctley
    """
    return cmp(int(element1), int(element2))


def missing_rate(data, missing_tag=['*', '?', '-1', '-7', '-8', '-9']):
    mr = 0.0
    mrr = 0.0
    att_m = []
    number_record = len(data)
    r_len = len(data[0]) - 1
    att_m = [False] * r_len
    for record in data:
        flag = False
        for index, t in enumerate(record):
            if t in missing_tag:
                mr += 1
                flag = True
                att_m[index] = True
        if flag:
            mrr += 1
    mr = mr * 100.0 / (number_record * r_len)
    print "Number of missing records", mrr
    mrr = mrr * 100.0 / number_record
    print "Missing Rate %.2f%%" % mr
    print "Missing Record Rate  %.2f%%" % mrr
    print "Attribute with missing value", att_m
