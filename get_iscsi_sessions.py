#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.4 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""

import json
import sys
from modules.choose_inputs import get_inputs_search_id as get_inputs
from modules.build_auth import build_auth
from modules.connect_cluster import connect_cluster_rest as connect_cluster
from modules.build_table import autosized_table as build_table

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


def get_iscsi_session_info(headers, url, search_id=None):
    """
    Get the iSCSI sessions
    """
    vol_id_array = {}
    iscsi_session_list = []
    sessions_lists = []
    node_dict = node_dict = get_node_list(headers, url)
    payload = json.dumps({"method": "ListISCSISessions", "params":{}, "id": 1})
    response_json = connect_cluster(headers, url, payload)
    for iqn in response_json['result']['sessions']:
        session_id = iqn['sessionID']
        initiator_name = iqn['initiatorName']
        node_id = iqn['nodeID']
        node_name = node_dict[node_id]
        if node_id in vol_id_array.keys():
            vol_id_array[node_id] = vol_id_array[node_id] + 1
        else:
            vol_id_array[node_id] = 1
        target_name = iqn['targetName']
        target_host = (target_name.split(".")[0] + "."
                       + target_name.split(".")[1] + "."
                       + target_name.split(".")[2] + "."
                       + target_name.split(".")[3])
        vol_name = target_name.split(".")[4]
        vol_id = target_name.split(".")[5]
        iscsi_session_list = [session_id, node_id, node_name, vol_id,
                              vol_name, initiator_name, target_host]
        if search_id is not None:
            if search_id in iscsi_session_list:
                sessions_lists.append(iscsi_session_list)
        else:
            sessions_lists.append(iscsi_session_list)


    if len(vol_id_array) == 0:
        print("No iSCSI sessions returned, script will now exit")
        sys.exit(1)

    return sessions_lists


def get_table_headers():
    """
    Build the table headers
    """
    hdr1 = "Session ID"
    hdr2 = "Node ID"
    hdr3 = "Node Name"
    hdr4 = "Volume ID"
    hdr5 = "Volume Name"
    hdr6 = "Initiator"
    hdr7 =  "Target Host"
    hdr_list = [hdr1, hdr2, hdr3, hdr4, hdr5, hdr6, hdr7]
    return hdr_list


def main():
    """
    Execute the functions from above
    """
    mvip, user, user_pass, mvip_node, search_id = get_inputs()
    headers, url = build_auth(mvip, user, user_pass, mvip_node)
    iscsi_session_array = get_iscsi_session_info(headers, url, search_id)
    hdr_list = get_table_headers()
    build_table(hdr_list, iscsi_session_array)

if __name__ == "__main__":
    main()
