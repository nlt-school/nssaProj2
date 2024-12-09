#!/bin/python3 

import pandas as pd
import numpy as np

def compute_metrics(data, node_ip):
    requests = data[data["Ping"].str.contains("request", case=False, na=False)]
    replies = data[data["Ping"].str.contains("reply", case=False, na=False)]

    request_reply_pairs = pd.merge(
        requests,
        replies,
        left_on=["seq"],
        right_on=["seq"],
        suffixes=("_req", "_rep")
    )
    request_reply_pairs = request_reply_pairs[request_reply_pairs["Source_req"] == node_ip]

    rtt_values = (request_reply_pairs["Time_rep"] - request_reply_pairs["Time_req"]).abs()
    total_rtt = rtt_values.sum()

    metrics = {
        "Echo Requests Sent": len(requests[requests["Source"] == node_ip]),
        "Echo Requests Received": len(requests[requests["Destination"] == node_ip]),
        "Echo Replies Sent": len(replies[replies["Source"] == node_ip]),
        "Echo Replies Received": len(replies[replies["Destination"] == node_ip]),
        "Echo Request Bytes Sent (bytes)": requests[requests["Source"] == node_ip]["Length"].sum(),
        "Echo Request Bytes Received (bytes)": requests[requests["Destination"] == node_ip]["Length"].sum(),
    }

    icmp_payload_size = 28
    metrics["Echo Request Data Sent (bytes)"] = (
        metrics["Echo Request Bytes Sent (bytes)"] - metrics["Echo Requests Sent"] * icmp_payload_size
    )
    metrics["Echo Request Data Received (bytes)"] = (
        metrics["Echo Request Bytes Received (bytes)"] - metrics["Echo Requests Received"] * icmp_payload_size
    )

    metrics["Average RTT (milliseconds)"] = rtt_values.mean() * 1000 if not rtt_values.empty else 0

    total_time = request_reply_pairs["Time_rep"].max() - request_reply_pairs["Time_req"].min() if not request_reply_pairs.empty else 1
    metrics["Echo Request Throughput (kB/sec)"] = (metrics["Echo Request Bytes Sent (bytes)"] / 1024) / total_time if total_time > 0 else 0
    metrics["Echo Request Goodput (kB/sec)"] = (metrics["Echo Request Data Sent (bytes)"] / 1024) / total_time if total_time > 0 else 0

    request_reply_pairs["ttl_req"] = pd.to_numeric(request_reply_pairs["ttl_req"].str.split().str[0], errors="coerce")
    hop_counts = 128 - request_reply_pairs["ttl_req"]
    hop_counts = hop_counts.dropna()  # Remove NaN values (invalid TTLs)
    metrics["Average Echo Request Hop Count"] = hop_counts.mean() if not hop_counts.empty else np.nan


    reply_delays = (request_reply_pairs["Time_rep"] - request_reply_pairs["Time_req"]).abs()
    metrics["Average Reply Delay (microseconds)"] = reply_delays.mean() * 1e6 if not reply_delays.empty else 0

    return metrics

def format_output(data):
    output = []
    for node, metrics in data.items():
        output.append(f"{node}\n")
        output.append("Echo Requests Sent\tEcho Requests Received\tEcho Replies Sent\tEcho Replies Received\n")
        output.append(f"{metrics['Echo Requests Sent']}\t{metrics['Echo Requests Received']}\t{metrics['Echo Replies Sent']}\t{metrics['Echo Replies Received']}\n")
        output.append("Echo Request Bytes Sent (bytes)\tEcho Request Data Sent (bytes)\n")
        output.append(f"{metrics['Echo Request Bytes Sent (bytes)']}\t{metrics['Echo Request Data Sent (bytes)']}\n")
        output.append("Echo Request Bytes Received (bytes)\tEcho Request Data Received (bytes)\n")
        output.append(f"{metrics['Echo Request Bytes Received (bytes)']}\t{metrics['Echo Request Data Received (bytes)']}\n\n")
        output.append(f"Average RTT (milliseconds)\t{metrics['Average RTT (milliseconds)']}\n")
        output.append(f"Echo Request Throughput (kB/sec)\t{metrics['Echo Request Throughput (kB/sec)']}\n")
        output.append(f"Echo Request Goodput (kB/sec)\t{metrics['Echo Request Goodput (kB/sec)']}\n")
        output.append(f"Average Reply Delay (microseconds)\t{metrics['Average Reply Delay (microseconds)']}\n")
        output.append(f"Average Echo Request Hop Count\t{metrics['Average Echo Request Hop Count']}\n\n")
    return ''.join(output)

def process_files(file_paths, node_ips):
    results = {}
    for file_path, node_ip in zip(file_paths, node_ips):
        data = pd.read_csv(file_path)
        metrics = compute_metrics(data, node_ip)
        results[f"Node {node_ips.index(node_ip) + 1}"] = metrics
    return results

if __name__ == "__main__":
    file_paths = ["parsed/Node1_parsed.csv", "parsed/Node2_parsed.csv", "parsed/Node3_parsed.csv", "parsed/Node4_parsed.csv"]
    node_ips = ["192.168.100.1", "192.168.100.2", "192.168.200.1", "192.168.200.2"]

    metrics = process_files(file_paths, node_ips)
    output = format_output(metrics)

    with open("Final_Output.csv", "w") as f:
        f.write(output)
