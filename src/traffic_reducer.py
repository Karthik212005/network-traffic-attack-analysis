#!/usr/bin/env python3

import sys

current_label = None
duration_sum = 0.0
packet_sum = 0.0
count = 0

def output_result():
    if current_label is not None and count > 0:
        avg_duration = duration_sum / count
        avg_packets = packet_sum / count

        print(
            f"{current_label}\t{count}\t"
            f"{avg_duration:.2f}\t{avg_packets:.2f}"
        )

for line in sys.stdin:
    try:
        label, duration, packets, record_count = (
            line.rstrip("\n").split("\t")
        )

        duration = float(duration)
        packets = float(packets)
        record_count = int(record_count)

    except ValueError:
        continue

    if current_label != label:
        output_result()

        current_label = label
        duration_sum = 0.0
        packet_sum = 0.0
        count = 0

    duration_sum += duration
    packet_sum += packets
    count += record_count

output_result()
