#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.6 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""
import json
from modules.choose_inputs import get_inputs_default as get_inputs
from modules.build_auth import build_auth
from modules.connect_cluster import connect_cluster_rest as connect_cluster


def build_master_id_payload():
    """
    Build the API payload
    """
    master_id_payload = json.dumps({"method": "GetClusterMasterNodeID",
                                    "params": {}, "id": 1})
    return master_id_payload


def build_ensemble_id_payload():
    """
    Build the API payload
    """
    ensemble_id_payload = json.dumps({"method": "TestLocateCluster",
                                      "params": {"force": True}, "id": 1})
    return ensemble_id_payload


def build_node_list_payload():
    """
    Build the active node API payload
    """
    node_list_payload = json.dumps({"method": "ListAllNodes",
                                    "params": {"force": True}, "id": 1})
    return node_list_payload


def get_master_id(response_json):
    """
    Get the master node ID and return it for comparison against active nodes
    """
    master_json = response_json
    master_id = master_json['result']['nodeID']
    return master_id


def get_active_nodes(response_json):
    """
    Get the active node list and parse for ID and namne
    return node_dict for comparison
    """
    node_dict = {}
    node_list_json = response_json
    for node in node_list_json['result']['nodes']:
        node_id = node['nodeID']
        node_name = node['name']
        node_dict[node_id] = node_name
    return node_dict


def master_locator(master_id, node_dict, ensemble_dict):
    """
    Identify the master
    """
    output_dict = {}
    ensemble_keys = ensemble_dict.keys()
    for key, value in node_dict.items():
        if key == master_id:
            output_dict["Master"] = value
        if key in ensemble_keys:
            output_dict[key] = node_dict[key]
    print("+" + "-"*12 + "+" + "-"*28 + "+")
    for key, val in output_dict.items():
        print("|" + str(key).rjust(12) + "|" + val.rjust(28) + "|")
    print("+" + "-"*12 + "+" + "-"*28 + "+")


def get_ensemble(response_json):
    """test"""
    ensemble_dict = {}
    ensemble_list_json = response_json
    for node in ensemble_list_json['result']['nodes']:
        for nodes in node['result']['details']['ensemble']['nodes']:
            node_ip = nodes['IP']
            node_id = nodes['nodeID']
            ensemble_dict[node_id] = node_ip
    return ensemble_dict


def main():
    """
    Execute the functions from above
    """
    mvip, user, user_pass, mvip_node = get_inputs()
    headers, url = build_auth(mvip, user, user_pass, mvip_node)
    master_id_payload = build_master_id_payload()
    ensemble_id_payload = build_ensemble_id_payload()
    node_list_payload = build_node_list_payload()
    response_json = connect_cluster(headers, url, master_id_payload)
    master_id = get_master_id(response_json)
    response_json = connect_cluster(headers, url, node_list_payload)
    node_dict = get_active_nodes(response_json)
    response_json = connect_cluster(headers, url, ensemble_id_payload)
    ensemble_dict = get_ensemble(response_json)
    master_locator(master_id, node_dict, ensemble_dict)


if __name__ == "__main__":
    main()
