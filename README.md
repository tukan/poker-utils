poker-utils
===========

Small poker utils I use in my workaround

## search_hand.py

Small script for searching hand by its game id in directory or list of files, it's pretty dump and the marker of
start of the hand is just a line contains the game id and the marker of the end of the hand is an empty (stripped) line
or EOF


### Example

```
python search_hand.py -d . 11111111111
```

Will output:

```
Found in file: /Users/tukan/hands/test_sample/File125.txt
PokerStars Hand #11111111111:  Omaha Pot Limit ($2/$4 USD) - 2010/07/26 6:17:21 ET
Table 'Ricarda' 6-max Seat #6 is the button
Seat 1: player_1 ($278.50 in chips)
Seat 2: player_2 ($453.30 in chips)
Seat 3: player_3 ($552 in chips)
Seat 5: player_5 ($315.50 in chips)
Seat 6: player_6 ($446.95 in chips)
player_1: posts small blind $2
player_2: posts big blind $4
shock3r: sits out
*** HOLE CARDS ***
Dealt to player_6 [6d Kh 5d Jh]
player_3: folds
player_5: raises $10 to $14
player_6: folds
player_1: folds
player_2: folds
Uncalled bet ($10) returned to player_5
player_5 collected $10 from pot
*** SUMMARY ***
Total pot $10 | Rake $0
Seat 1: player_1 (small blind) folded before Flop
Seat 2: player_2 (big blind) folded before Flop
Seat 3: player_3 folded before Flop (didn't bet)
Seat 5: player_5 collected ($10)
Seat 6: player_6 (button) folded before Flop (didn't bet)
```

### Usage

```
python search_hand.py --help
```

```
usage: search_hand [-h] [-d DIR] [-f FILES] [-o OUT] [--no-progressbar]
                   [--find-all] [--version]
                   hand_id

Searches a hand(s) by a hand_id in a directory or in a list of files

positional arguments:
  hand_id               Hand (or game) id

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     directory with hand history files
  -f FILES, --files FILES
                        list hand history files
  -o OUT                file name to print found hands (by default stdout)
  --no-progressbar      don't print a progressbar
  --find-all            search for all occurrences of the hand_id
  --version             show program's version number and exit
```