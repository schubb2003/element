#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.4 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""

import json
import sys
from modules.choose_inputs import get_inputs_default as get_inputs
from modules.build_auth import build_auth
from modules.connect_cluster import connect_cluster_rest as connect_cluster
from modules.build_table import build_table_dual_column_dict as build_table

def get_node_list(headers, url):
    """
    Build the list of nodes
    """
    node_dict = {}
    payload = json.dumps({"method": "ListActiveNodes", "params":{}, "id": 1})
    response_json = connect_cluster(headers, url, payload)
    for node in response_json['result']['nodes']:
        node_name = node['name']
        node_id = node['nodeID']
        node_dict[node_id] = node_name
    return node_dict


def get_iscsi_session_info(headers, url):
    """
    Get the iSCSI sessions
    """
    vol_id_array = {}
    node_session_array = {}
    node_dict = node_dict = get_node_list(headers, url)
    payload = json.dumps({"method": "ListISCSISessions", "params":{}, "id": 1})
    response_json = connect_cluster(headers, url, payload)
    for iqn in response_json['result']['sessions']:
        initiator_name = iqn['initiatorName']
        node_id = iqn['nodeID']
        if node_id in vol_id_array.keys():
            vol_id_array[node_id] = vol_id_array[node_id] + 1
        else:
            vol_id_array[node_id] = 1
        target_name = iqn['targetName']
        vol_id = target_name.split(".")[5]
    if len(vol_id_array) == 0:
        print("No iSCSI sessions returned, script will now exit")
        sys.exit(1)
    for key in vol_id_array:
        node_name = node_dict[key]
        node_session_array[node_name] = vol_id_array[key]
    return node_session_array


def get_table_headers():
    """
    Build the table headers
    """
    hdr1 = "Node Name"
    hdr2 = "iSCSI session count"
    return hdr1, hdr2


def main():
    """
    Execute the functions from above
    """
    mvip, user, user_pass, mvip_node = get_inputs()
    headers, url = build_auth(mvip, user, user_pass, mvip_node)
    node_session_array = get_iscsi_session_info(headers, url)
    hdr1, hdr2 = get_table_headers()
    build_table(hdr1, hdr2, node_session_array)


if __name__ == "__main__":
    main()
