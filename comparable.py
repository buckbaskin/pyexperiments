#!/usr/bin/env python

import sys
import string

def get_file_names():
    '''
    Get the file names from the command line (with default arguments)
    '''
    base = 'base.txt'
    compare = 'compare.txt'
    for index, value in enumerate(sys.argv):
        if index == 0:
            continue
        elif index == 1:
            base = str(value)
        elif index == 2:
            compare = str(value)
        break
    return (base, compare,)

def to_histogram(file):
    '''
    Accumulate how many times each word shows up in the document
    '''
    histogram = {}
    for line in file:
        for word in line.split(' '):
            word = word.lower().strip(string.whitespace + string.punctuation)
            if len(word) <= 0:
                continue
            if word not in histogram:
                histogram[word] = 0
            histogram[word] += 1
    return histogram

def compare_histograms(base, compare):
    '''
    Returns a histogram with the diff of the two (compare - base)
    '''
    only_comp = {}
    more_comp = {}
    same = {}
    more_base = {}
    only_base = {}
    
    for word in base:
        if word not in compare:
            only_base[word] = base[word]
        else:
            diff = compare[word] - base[word]
            if diff > 0:
                more_comp[word] = diff
            elif diff < 0:
                more_base[word] = -diff
            else:
                same[word] = 0
    for word in compare:
        if word not in base:
            only_comp[word] = compare[word]

    return {
        'only_comp': only_comp,
        'more_comp': more_comp,
        'same': same,
        'more_base': more_base,
        'only_base': only_base,
    }

def display_sorted_histogram(histogram):
    sorted_word_count = sorted(list(histogram.items()), key=lambda w: w[0])
    sorted_word_count = sorted(sorted_word_count, key=lambda w: w[1])

    # list sorted by word count, then alphabetically

    for word, word_count in sorted_word_count:
        word = word.ljust(20)
        print('%s %3d' % (word, word_count,))

def display_report(only_comp, more_comp, same, more_base, only_base):
    print('Hello Comparator')
    print('These words were only found in the base file')
    display_sorted_histogram(only_base)

    print('These words were only found in the compare file')
    display_sorted_histogram(only_comp)

    print('These words were found more often in the base file')
    display_sorted_histogram(more_base)

    print('These words were found more often in the compare file')
    display_sorted_histogram(more_comp)

    print('These words were found the same number of times in both files')
    display_sorted_histogram(same)


if __name__ == '__main__':
    baseName, compName = get_file_names()

    with open(baseName, 'r') as baseFile:
        baseHistogram = to_histogram(baseFile)

    with open(compName, 'r') as compFile:
        compHistogram = to_histogram(compFile)

    display_report(**compare_histograms(baseHistogram, compHistogram))