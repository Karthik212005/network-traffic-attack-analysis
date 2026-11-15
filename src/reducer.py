#!/usr/bin/env python3

import sys

current_label = None
current_count = 0

for line in sys.stdin:
    try:
        label, count = line.rstrip("\n").split("\t", 1)
        count = int(count)
    except ValueError:
        continue

    if current_label == label:
        current_count += count
    else:
        if current_label is not None:
            print(f"{current_label}\t{current_count}")

        current_label = label
        current_count = count

if current_label is not None:
    print(f"{current_label}\t{current_count}")
