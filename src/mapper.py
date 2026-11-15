#!/usr/bin/env python3

import sys
import csv

for line in sys.stdin:
    try:
        row = next(csv.reader([line]))

        # Skip header and invalid rows
        if len(row) != 79:
            continue

        label = row[-1].strip()

        if label.lower() == "label" or not label:
            continue

        # Emit attack label and count
        print(f"{label}\t1")

    except (csv.Error, UnicodeError):
        continue
