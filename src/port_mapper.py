#!/usr/bin/env python3

import sys
import csv

for line in sys.stdin:
    try:
        row = next(csv.reader([line]))

        if len(row) != 79:
            continue

        port = row[0].strip()
        label = row[-1].strip()

        if label.lower() == "label":
            continue

        if label.upper() == "BENIGN":
            continue

        port_number = int(port)

        if not 0 <= port_number <= 65535:
            continue

        print(f"{port_number}\t1")

    except (ValueError, csv.Error, UnicodeError):
        continue
