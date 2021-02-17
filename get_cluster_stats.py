#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.6 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
# This script gets the network config from a single node for a node replacment
"""

import json
from modules.choose_inputs import get_inputs_default as get_inputs
from modules.build_auth import build_auth
from modules.connect_cluster import connect_cluster_rest as connect_cluster
from modules.build_table import autosized_table_two_column as build_table


def build_payload():
    """
    Build the payload for the API
    """
    payload = json.dumps({"method": "GetClusterStats", "params":{}, "id": 1})
    return payload


def build_output(mvip, response_json):
    #print(json.dumps(response_json, indent=4, sort_keys=True))
    cls_stat_dict = {}
    cls_stats = response_json['result']['clusterStats']
    actual_iops = cls_stats['actualIOPS']
    avg_iop_size = cls_stats['averageIOPSize']
    clnt_queue_depth = cls_stats['clientQueueDepth']
    cls_util = cls_stats['clusterUtilization']
    latency_usec = cls_stats['latencyUSec']
    normd_iops = cls_stats['normalizedIOPS']
    read_bytes = cls_stats['readBytes']
    read_bytes_last = cls_stats['readBytesLastSample']
    read_usec = cls_stats['readLatencyUSec']
    read_usec_total = cls_stats['readLatencyUSecTotal']
    read_ops = cls_stats['readOps']
    read_ops_last = cls_stats['readOpsLastSample']
    time_stamp = cls_stats['timestamp']
    unalign_read = cls_stats['unalignedReads']
    unalign_write = cls_stats['unalignedWrites']
    write_bytes = cls_stats['writeBytes']
    write_bytes_last = cls_stats['writeBytesLastSample']
    write_usec = cls_stats['writeLatencyUSec']
    write_usec_total = cls_stats['writeLatencyUSecTotal']
    write_ops = cls_stats['writeOps']
    write_ops_last = cls_stats['writeOpsLastSample']
    # Build the dictionary for output
    cls_stat_dict["Actual IOPS"] = actual_iops
    cls_stat_dict["Average IO Size"] = avg_iop_size
    cls_stat_dict["Client Queue Depth"] = clnt_queue_depth
    cls_stat_dict["Cluster Utilization"] = cls_util
    cls_stat_dict["Latency in Usec"] = latency_usec
    cls_stat_dict["Normalized IOPS"] = normd_iops
    cls_stat_dict["Read Bytes"] = read_bytes
    cls_stat_dict["Read Bytes in Last Sample"] = read_bytes_last
    cls_stat_dict["Read Usec"] = read_usec
    cls_stat_dict["Read Usec Total"] = read_usec_total
    cls_stat_dict["Read Ops"] = read_ops
    cls_stat_dict["Read Ops in Last Sample"] = read_ops_last
    cls_stat_dict["Timestamp"] = time_stamp
    cls_stat_dict["Unaligned Reads"] = unalign_read
    cls_stat_dict["Unaligned Writes"] = unalign_write
    cls_stat_dict["Write Bytes"] = write_bytes
    cls_stat_dict["Write Bytes in Last Sample"] = write_bytes_last
    cls_stat_dict["Write Usec"] = write_usec
    cls_stat_dict["Write Usec Total"] = write_usec_total
    cls_stat_dict["Write Ops"] = write_ops
    cls_stat_dict["Write Ops in Last Sample"] = write_ops_last
    return cls_stat_dict


def main():
    """
    Execute the above functions
    """
    mvip, user, user_pass, mvip_node = get_inputs()
    headers, url = build_auth(mvip, user, user_pass, mvip_node)
    payload = build_payload()
    response_json = connect_cluster(headers, url, payload)
    cls_stat_dict = build_output(mvip, response_json)
    build_table(cls_stat_dict)


if __name__ == "__main__":
    main()
