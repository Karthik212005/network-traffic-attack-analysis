#!/usr/bin/env python3

import sys
import csv
import math

for line in sys.stdin:
    try:
        row = next(csv.reader([line]))

        if len(row) != 79:
            continue

        label = row[78].strip()

        if not label or label.lower() == "label":
            continue

        duration = float(row[1])
        fwd_packets = float(row[2])
        bwd_packets = float(row[3])

        if not all(math.isfinite(x) for x in
                   (duration, fwd_packets, bwd_packets)):
            continue

        total_packets = fwd_packets + bwd_packets

        print(f"{label}\t{duration}\t{total_packets}\t1")

    except (ValueError, csv.Error, UnicodeError):
        continue
