#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
from os.path import join as file_join, abspath
import progressbar


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='search_hand',
        description='Searches a hand(s) by a hand_id in a directory or in a list of files'
    )
    parser.add_argument('hand_id', metavar='hand_id', type=str, help='Hand (or game) id')
    parser.add_argument('-d', '--dir', type=str, dest='dir', help='directory with hand history files')
    parser.add_argument('-f', '--files', type=str, dest='files', help='list hand history files')
    parser.add_argument('-o', type=str, dest='out', help='file name to print found hands (by default stdout)')
    parser.add_argument('--no-progressbar', action="store_true", dest='no_progressbar',
                        help='don\'t print a progressbar')
    parser.add_argument('--find-all', action="store_true", help='search for all occurrences of the hand_id')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    files = []
    if args.dir is not None:
        for f in os.listdir(args.dir):
            files.append(file_join(args.dir, f))
    elif args.files is not None:
        files = args.files
    else:
        parser.print_help()
        exit(1)

    hand_id = args.hand_id
    find_all = args.find_all
    out = sys.stdout if args.out is None else open(args.out, 'wb')
    files_iter = progressbar.ProgressBar()(files) if not args.no_progressbar else files

    for fname in files_iter:
        in_hand = False
        f = open(fname, 'rb')
        line = f.readline(1000)

        while len(line) > 0:
            if in_hand:
                if len(line.strip()) > 0:
                    print >>out, line.rstrip()
                else:
                    print >>out
                    print >>out
                    in_hand = False
                    if not find_all:
                        exit(0)
            else:
                # As far as I know Python uses Use Boyer-Moore-Horspool algorithm to search a substring in a string,
                # here is a link to Python svn repo:
                # http://svn.python.org/view/python/trunk/Objects/stringlib/fastsearch.h?revision=77470&view=markup
                in_hand = hand_id in line
                if in_hand:
                    print >>out, "Found in file:", abspath(fname)
                    print >>out, line.rstrip()

            line = f.readline(1000)
        f.close()

    out.close()