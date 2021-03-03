#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.6 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
# This script gets the network config from a single node for a node replacment
"""
import json
from prettytable import PrettyTable
from modules.choose_inputs import get_inputs_default as get_inputs
from modules.build_auth import build_auth
from modules.connect_cluster import connect_cluster_rest as connect_cluster
from get_hardware_config import build_payload as get_hw_payload


def build_payload():
    """
    Build the payload for the API
    """
    payload = json.dumps({"method": "ListDrives", "params": {}, "id": 1})
    return payload


def parse_drives(response_json, node_dict):
    """
    Determine how many drives are being reported, compare against how many
      should exist, return dictionaries of active/failed/missing as well as
      print the information out to the screen
      """
    failed_count = 0
    active_count = 0
    total_missing = 0
    node_list = []
    failed_drive_dict = {}
    active_drive_dict = {}
    missing_drive_dict = {}
    drive_res = response_json['result']['drives']
    for drive in drive_res:
        drive_node = drive['nodeID']
        drive_id = drive['driveID']
        node_list.append(drive_node)
        drive_key = str(drive_node) + "_" + str(drive_id)
        drive_status = drive['status']
        if drive_status == "failed":
            failed_count = failed_count + 1
            failed_drive_dict[drive_key] = "failed"
        if drive_status == "active":
            active_count = active_count + 1
            active_drive_dict[drive_key] = "active"
    for node_key, node_val in node_dict.items():
        missing_count = 0
        node_disk_count = node_dict[node_key] - node_list.count(node_key)
        if node_list.count(node_key) == node_dict[node_key]:
            print(f"disk count matches for node ID {node_key}")
        else:
            print(f"disk count mismatch for node ID {node_key}")
            missing_count = missing_count + node_disk_count
            total_missing = total_missing + missing_count
            missing_drive_dict[node_key] = {"misisngCount": missing_count}
            print(f"Missing count is: {missing_count}")
    if len(missing_drive_dict) != 0:
        print(f"Missing dict:\t{missing_drive_dict}")
    print_table(active_drive_dict, failed_drive_dict)

    return active_drive_dict, failed_drive_dict, missing_drive_dict


def parse_hw_config(hw_config_response):
    """
    Needed to make sure we compare the right number of slots to the returned
      information.  SF series is 10 slots, H series is 12... need to be able
      to adjust automatically
    This will work on a system with MDSS in effect as we read the slots
      presented from the GetHardwareConfig output
    """
    node_dict = {}
    hw_res = hw_config_response['result']['nodes']
    for node in hw_res:
        node_id = node['nodeID']
        block_slot_list = node['result']['hardwareConfig']['blockDrives']
        meta_slot_list = node['result']['hardwareConfig']['sliceDrives']
        slot_count = len(block_slot_list) + len(meta_slot_list)
        node_dict[node_id] = slot_count
    return node_dict


def get_hw_response(headers, url, hw_payload):
    pass


def print_table(active_drive_dict, failed_drive_dict):
    drive_table = PrettyTable()
    drive_table.field_names = ("Node ID", "Drive ID", "State")
    for drive_out in active_drive_dict, failed_drive_dict:
        for drive_key, drive_val in drive_out.items():
            node_id = drive_key.split("_")[0]
            drive_id = drive_key.split("_")[1]
            drive_table.add_row([node_id, drive_id, drive_val])

    print(drive_table.get_string(sortby="Node ID"))


def main():
    """
    Call the above functions
    """
    mvip, user, user_pass, mvip_node = get_inputs()
    headers, url = build_auth(mvip, user, user_pass, mvip_node)
    hw_payload = get_hw_payload()
    hw_config_response = connect_cluster(headers, url, hw_payload)
    node_dict = parse_hw_config(hw_config_response)
    payload = build_payload()
    response_json = connect_cluster(headers, url, payload)
    (active_drive_dict,
     failed_drive_dict,
     missing_drive_dict) = parse_drives(response_json, node_dict)


if __name__ == "__main__":
    main()
