#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.6 and above
# No warranty is offered, use at your own risk.
# While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
# -i, -a, and -e are exclusive, using -e ignores any setting of -i or -a
# Usage examples:
# Example 1, using account ID for lookup:
#   python get_vol_primary_service_id.py -m cluster1 -u admin -i 4
# Enter password for user admin on cluster cluster1:
# Gathering information from: ListVolumes
# Gathering information from: ListVolumeStats
# +-----------+------------+
# | Volume ID | Service ID |
# +-----------+------------+
# |     8     |     10     |
# |     9     |     44     |
# |     10    |     10     |
# |     11    |     48     |
# |     12    |     10     |
# |     13    |     48     |
# |     14    |     48     |
# +-----------+------------+
# Example 2, using account name for lookup:
#   python get_vol_primary_service_id.py -m cluster1 -u admin -a acct1
# Enter password for user admin on cluster cluster1:
# Gathering information from: ListVolumes
# Gathering information from: ListVolumeStats
# Gathering information from: GetAccountByName
# +-----------+------------+
# | Volume ID | Service ID |
# +-----------+------------+
# |     8     |     10     |
# |     9     |     44     |
# |     10    |     10     |
# |     11    |     48     |
# |     12    |     10     |
# |     13    |     48     |
# |     14    |     48     |
# +-----------+------------+
"""

import json
from prettytable import PrettyTable
from modules.choose_inputs import get_inputs_service_info as get_inputs
from modules.build_auth import build_auth
from modules.connect_cluster import connect_cluster_rest as connect_cluster


def build_payload(call_vols, params):
    """
    Build the API payload
    """
    payload = json.dumps({"method": call_vols, "params": params, "id": 1})
    return payload


def get_outputs(headers, url, acct_name):
    """
    Generate output to provide to the table
    """
    # Need all four of these API calls to merge the required data together
    output_dict = {}
    api_call_vols = ["ListVolumes", "ListVolumeStats",
                     "ListAllNodes", "ListServices"]
    if acct_name is not None:
        api_call_vols.append("GetAccountByName")
    for call_vols in api_call_vols:
        if call_vols == "GetAccountByName":
            params = {"username": acct_name}
        else:
            params = {"force": True}
        print(f"Gathering information from: {call_vols}")
        payload = build_payload(call_vols, params)
        response_json = connect_cluster(headers, url, payload)
        output_dict[call_vols] = response_json
    return output_dict


def get_node_info(**output_dict):
    """
    put something here to stop linting from alerting
    """
    nodes_dict = {}
    services_dict = {}
    node_out_dict = {}
    all_nodes_json = output_dict['ListAllNodes']
    services_json = output_dict['ListServices']
    # Build a dict of all service IDs and node IDs
    for service in services_json['result']['services']:
        if service['service']['serviceType'] == "slice":
            node_id = service['node']['nodeID']
            service_id = service['service']['serviceID']
            services_dict[node_id] = service_id
    # Build a dict of node IDs and node names
    for node in all_nodes_json['result']['nodes']:
        node_id = node['nodeID']
        node_name = node['name']
        nodes_dict[node_id] = node_name
    # Loop through the two dicts above and if the keys match create a new dict
    #  with node ID as the key, with node name and service ID in a list as the
    #  key value
    node_keys = nodes_dict.keys()
    for key in node_keys:
        if key in nodes_dict.keys():
            node_out_dict[key] = (node_id, nodes_dict[key], services_dict[key])
    return node_out_dict


def get_account_id(**output_dict):
    """
    Get the account ID for volume lookup
    """
    try:
        response_json = output_dict['GetAccountByName']
        acct_id = response_json['result']['account']['accountID']
        return acct_id
    except TypeError:
        # Handle when an account does not exist
        print(f"\nAccount name for volume not found,"
              f" please verify and try again\n")


def get_account_volumes(acct_id, all_vols, **output_dict):
    """
    Get a list of volumes and the account id
    """
    vol_dict = {}
    response_json = output_dict['ListVolumes']
    for vol in response_json['result']['volumes']:
        if all_vols is False:
            if vol['accountID'] == acct_id:
                vol_id = vol['volumeID']
                vol_name = vol['name']
                vol_dict[vol_id] = vol_name
        else:
            vol_id = vol['volumeID']
            vol_name = vol['name']
            vol_dict[vol_id] = vol_name
    return vol_dict


def get_volume_slices(vol_dict, all_vols, **output_dict):
    """
    Parse out the volume slice information
    """
    out_dict = {}
    response_json = output_dict['ListVolumeStats']
    for vol in response_json['result']['volumeStats']:
        vol_id = vol['volumeID']
        if all_vols is False:
            if vol['volumeID'] in vol_dict.keys():
                vol_name = vol_dict[vol_id]
                vol_pri = vol['metadataHosts']['primary']
                out_dict[vol_id] = [vol_pri, vol_name]
        else:
            vol_name = vol_dict[vol_id]
            vol_pri = vol['metadataHosts']['primary']
            out_dict[vol_id] = [vol_pri, vol_name]
    return out_dict


def get_merge_dict(node_out_dict, vol_out_dict):
    """
    put something here to stop linting from alerting
    """
    out_dict = {}
    for vol_key, vol_val in vol_out_dict.items():
        for node_key, node_val in node_out_dict.items():
            if vol_val[0] == node_val[2]:
                vol_name = vol_val[1]
                vol_id = vol_key
                node_id = node_key
                node_name = node_val[1]
                vol_svc_id = node_val[2]
                out_dict[vol_name] = [vol_id, node_id,
                                      node_name, vol_svc_id]
    hdr1 = "Volume ID"
    hdr2 = "Volume Name"
    hdr3 = "Node ID"
    hdr4 = "Node Name"
    hdr5 = "Service ID"
    return hdr1, hdr2, out_dict, hdr3, hdr4, hdr5


def get_slice_counts(out_dict):
    """
    Add up the slice count per service id
    """
    slice_dict = {}
    my_list = []
    for val in out_dict.values():
        my_list.append(val[2])
    for primary in my_list:
        slice_count = 0
        for val in out_dict.values():
            if str(primary) == str(val[2]):
                slice_count = slice_count + 1
        slice_dict[primary] = slice_count
    hdr1 = "Primary ID"
    hdr2 = "Slice count"
    return hdr1, hdr2, slice_dict


def build_table(hdr1, hdr2, out_dict, hdr3=None, hdr4=None, hdr5=None):
    """
    Build the table for display
    """
    # Build two tables, one for the all vols which has slice balance info
    #   and one that has the selected account info with more columns
    out_tbl = PrettyTable()
    if hdr3 is None:
        out_tbl.field_names = [hdr1, hdr2]
        for key, val in out_dict.items():
            out_tbl.add_row([key, val])
    else:
        out_tbl.field_names = [hdr1, hdr2, hdr3, hdr4, hdr5]
        for key, val in out_dict.items():
            vol_name = key
            vol_id = val[0]
            node_id = val[1]
            node_name = val[2]
            service_id = val[3]
            out_tbl.add_row([vol_id, vol_name, node_id, node_name, service_id])
    print(f"{out_tbl}")


def main():
    """
    Call the function for output
    """
    mvip, user, user_pass, acct_id, acct_name, all_vols = get_inputs()
    headers, url = build_auth(mvip, user, user_pass)
    output_dict = get_outputs(headers, url, acct_name)
    node_out_dict = get_node_info(**output_dict)
    # Verify which output we are to provide, this is for single
    #   account out by account ID
    if acct_id is None and all_vols is False and acct_name is not None:
        acct_id = get_account_id(**output_dict)
    # This section gathers info for the all volume output
    vol_dict = get_account_volumes(acct_id, all_vols, **output_dict,)
    vol_out_dict = get_volume_slices(vol_dict, all_vols, **output_dict)
    hdr1, hdr2, out_dict, hdr3, hdr4, hdr5 = get_merge_dict(node_out_dict,
                                                            vol_out_dict)
    build_table(hdr1, hdr2, out_dict, hdr3, hdr4, hdr5)
    if all_vols is True:
        hdr1, hdr2, out_dict = get_slice_counts(out_dict)
        build_table(hdr1, hdr2, out_dict)


if __name__ == "__main__":
    main()
