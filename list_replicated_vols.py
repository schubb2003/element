#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.4 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
# This script gets the replication partner for a given cluster or all volumes
# Example successful outputs:
#   Volume -
#           Passed:
#           Total number of replication destinations is: {1}
#   Cluster -
#           +-----------------+--------------------+
#           | Cluster Pair ID |    Cluster Name    |
#           +-----------------+--------------------+
#           |        1        | SOLIDFIRE-IDN2-002 |
#           +-----------------+--------------------+
#           Passed: only one replication target
"""

import json
from prettytable import PrettyTable
from modules.choose_inputs import get_inputs_repl_cluster_or_vol as get_inputs
from modules.build_auth import build_auth
from modules.connect_cluster import connect_cluster_rest as connect_cluster

def build_payload(check_opt):
    """
    Build the payload for the API call
    """
    if check_opt == "cluster":
        payload = json.dumps({"method": "ListClusterPairs",
                              "params":{},
                              "id": 1})
    else:
        payload = json.dumps({"method": "ListActivePairedVolumes",
                              "params":{},
                              "id": 1})
    return payload


def build_table(cls_column1, cls_column2, cls_id, cls_name):
    """
    Build the output table for display
    """
    out_tbl = PrettyTable()
    out_tbl.field_names = [cls_column1, cls_column2]
    out_tbl.add_row([cls_id, cls_name])
    print(out_tbl)


def compare_pair_ids(response_json, check_opt):
    """
    Compare the cluser pairs
    """
    cluster_pair_count = []
    vol_pair_count = []
    if check_opt == "cluster":
        for cls_id in response_json['result']['clusterPairs']:
            cluster_pair_count.append(cls_id)
            cls_column1 = "Cluster Pair ID"
            cls_column2 = "Cluster Name"
            cls_id = cls_id['clusterPairID']
            cls_name = cls_id['clusterName']
            build_table(cls_column1, cls_column2, cls_id, cls_name)
        if (len(cluster_pair_count)) == 1:
            print("Passed: only one replication target")
        elif (len(cluster_pair_count)) > 1:
            print("Failed: more than one replication target")
        else:
            print("No replication found")
    else:
        for pair in response_json['result']['volumes']:
            for pair_id in pair['volumePairs']:
                if pair_id['remoteReplication']['state'] == "Unconfigured":
                    pass
                else:
                    vol_pair_count.append(pair_id['clusterPairID'])
        distinct_pair = set(vol_pair_count)
        array_len = len(distinct_pair)
        if array_len == 1:
            print("Passed:\nTotal number of "
                  "replication destinations is: {}".format(array_len))
        elif array_len > 1:
            print("Failed:\nTotal number of "
                  "replicaiton destinations is {}".format(array_len))
        else:
            print("No replication found")


def main():
    """
    Call the functions from above
    """
    mvip, user, user_pass, check_opt = get_inputs()
    headers, url = build_auth(mvip, user, user_pass)
    payload = build_payload(check_opt)
    response_json = connect_cluster(headers, url, payload)
    compare_pair_ids(response_json, check_opt)

if __name__ == "__main__":
    main()
