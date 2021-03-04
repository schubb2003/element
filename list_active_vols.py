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
from modules.build_table import autosized_table_one_row as build_table


def build_payload():
    """
    Build the payload for the API
    """
    payload = json.dumps({"method": "ListActiveVolumes",
                          "params": {}, "id": 1})
    return payload


def build_output(response_json):
    """
    Build the volume dictionary for outputting later on
    """
    vol_dict = {}
    vol_res = response_json['result']['volumes']
    for vol_info in vol_res:
        vol_access = vol_info['access']
        vol_account = vol_info['accountID']
        vol_create = vol_info['createTime']
        vol_snapmirror = vol_info['enableSnapMirrorReplication']
        vol_iqn = vol_info['iqn']
        vol_last_access = vol_info['lastAccessTime']
        vol_last_io = vol_info['lastAccessTimeIO']
        vol_name = vol_info['name']
        vol_burst_qos = vol_info['qos']['burstIOPS']
        vol_max_qos = vol_info['qos']['maxIOPS']
        vol_min_qos = vol_info['qos']['minIOPS']
        vol_qos_policy = vol_info['qosPolicyID']
        vol_naa_id = vol_info['scsiNAADeviceID']
        vol_status = vol_info['status']
        vol_size_bytes = vol_info['totalSize']
        vol_size_gib = round((vol_size_bytes/1048576/1024), 2)
        vol_vvol_id = vol_info['virtualVolumeID']
        vol_access_groups = vol_info['volumeAccessGroups']
        vol_id = vol_info['volumeID']
        vol_pair = vol_info['volumePairs']
        vol_uuid = vol_info['volumeUUID']
        vol_dict[vol_name] = [vol_name, vol_id, vol_access, vol_account,
                              vol_create, vol_snapmirror, vol_iqn,
                              vol_last_access, vol_last_io, vol_burst_qos,
                              vol_max_qos, vol_min_qos, vol_qos_policy,
                              vol_naa_id, vol_status, vol_size_gib,
                              vol_vvol_id, vol_access_groups, vol_pair,
                              vol_uuid]
        tbl_headers = ["Name", "ID", "Access", "Account", "Created",
                       "Snapmirrored", "IQN", "Last Access", "Last IO",
                       "Burst QoS", "Max Qos", "Min Qos", "QoS Policy",
                       "NAA ID", "Status", "Size in GiB", "VVol ID",
                       "Access Groups", "Paired Vols", "UUID"]
    return tbl_headers, vol_dict


def main():
    """
    Call the functions created above
    """
    mvip, user, user_pass, mvip_node = get_inputs()
    headers, url = build_auth(mvip, user, user_pass, mvip_node)
    payload = build_payload()
    response_json = connect_cluster(headers, url, payload)
    tbl_headers, vol_dict = build_output(response_json)
    build_table(tbl_headers, vol_dict)

if __name__ == "__main__":
    main()
