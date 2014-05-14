#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Timothy N. Tsvetkov (email: timothy.tsvetkov@gmail.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import time

import argparse
import os
import re
import codecs
import progressbar


def build_money_regex(amount='amount', currency='currency'):
    return r'(?P<%s>[^\d]*)\s*(?P<%s>(\d*,?\d*)*\.?\d+)' % (currency, amount)


HEADER_REGEX = re.compile(
    r'PokerStars\s+(?P<game_sub_type>Home Game|Zoom)?\s*(Hand|Game)\s+'
    r'\#(?P<game_id>\d+)\:\s+'
    r'(\"\{o_club}Club \#(?P<club_id>\d+)\{c_club})?\s*'
    r'(?P<game_type>.*)\s+'
    r'\({sb}/{bb}\s*(?P<currency>\w+)?\)\s+'
    r'-\s+'
    r'(?P<date>.*)'.
    format(
        o_club='{',
        c_club='}',
        sb=build_money_regex('sb','sb_c'),
        bb=build_money_regex('bb','bb_c')),
    re.UNICODE
)
SEAT_REGEX = re.compile(
    r'Seat\s+(?P<seat>\d+)\s*\:\s*(?P<player>.*)\s+\({stack}.*\)'.
    format(stack=build_money_regex('stack')),
    re.UNICODE
)


def open_out(out_name, out_ext, batch, ix):
    fname = "%s_%s%s" % (out_name, ix, out_ext) if batch is not None and batch > 0 else out_name + out_ext
    return codecs.open(fname, 'wb', encoding='utf-8', errors='strict')


def filter_hands(hand_files, player, out_name, out_ext, batch):
    total_hands, hands_filtered = 0, 0
    batch_counter, batch_ix = 0, 0

    out = open_out(out_name, out_ext, batch, batch_ix)

    for fname in hand_files:
        in_hand = False
        in_seats = False
        after_seats = False
        found = False
        hand = u''
        f = codecs.open(fname, 'rb', encoding='utf-8', errors='replace')
        line = f.readline(1000)

        while len(line) > 0:
            if in_hand:
                # Reading hand
                if len(line.strip()) > 0:
                    # Not empty line, so we're still in hand
                    if not after_seats and not found:
                        # Haven't found player and haven't finished reading seats
                        match = SEAT_REGEX.match(line)
                        if match is not None:
                            in_seats = True
                            found = player == match.group('player')
                        else:
                            after_seats = in_seats
                            in_seats = False

                    hand += line.rstrip() + u"\n"
                else:
                    # Empty line, finishing reading current hand
                    if found:
                        print >>out, hand
                        hands_filtered += 1
                        batch_counter += 1

                    in_hand = False
                    in_seats = False
                    after_seats = False
                    found = False
                    hand = u''
            else:
                # Waiting for a new hand
                match = HEADER_REGEX.match(line)
                in_hand = match is not None
                if in_hand:
                    if batch is not None and batch > 0 and batch_counter >= batch:
                        batch_ix += 1
                        batch_counter = 0
                        out.close()
                        out = open_out(out_name, out_ext, batch, batch_ix)

                    hand += u"Found in file: %s\n" % os.path.abspath(fname)
                    hand += line.rstrip() + u"\n"
                    total_hands += 1

            line = f.readline(1000)
        f.close()

    out.close()

    return total_hands, hands_filtered


def main():
    parser = argparse.ArgumentParser(
        prog='filter_hands_by_player',
        description='Filters hands by player. Hands in file must be divided by an empty line.'
    )

    parser.add_argument('player', metavar='player', type=str, help='Player to filter by')
    parser.add_argument('-d', '--dir', type=str, dest='dir', help='directory with hand history files')
    parser.add_argument('-f', '--file', type=str, dest='file', help='hand history file')
    parser.add_argument('-o', type=str, dest='out', default='out.txt',
                        help='file name to print found hands (default: out.txt)')
    parser.add_argument('-b', '--batch', type=int, dest='batch', help='save by BATCH hands per file')
    parser.add_argument('--no-progressbar', action="store_true", dest='no_progressbar',
                        help='don\'t print a progressbar')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    files = []
    if args.dir is not None:
        for root, dirs, fs in os.walk(args.dir):
            files += [os.path.join(root, f) for f in fs]
    elif args.file is not None:
        files = [args.file]
    else:
        parser.print_help()
        exit(1)

    out_dir = os.path.dirname(args.out)
    if len(out_dir) > 0 and not os.path.exists(out_dir):
        os.makedirs(out_dir)

    basename = os.path.basename(args.out)
    fname, out_ext = os.path.splitext(basename)
    out_name = os.path.join(out_dir, fname)

    if not args.no_progressbar:
        widgets = [
            progressbar.Percentage(),
            ' ',
            progressbar.Bar(),
            ' ',
            progressbar.ETA()
        ]
        files_iter = progressbar.ProgressBar(widgets=widgets)(files)
    else:
        files_iter = files

    t0 = time.time()
    player = args.player.decode('utf-8')
    total_hands, hands_filtered = filter_hands(files_iter, player, out_name, out_ext, args.batch)
    t1 = time.time()

    print
    print "Filtered %d from %d hands" % (hands_filtered, total_hands)
    print "Total time: %f sec." % (t1 - t0)
    print


if __name__ == "__main__":
    main()
