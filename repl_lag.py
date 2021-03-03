#!/usr/bin/python
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.6 and above
# No warranty is offered, use at your own risk.  While these scripts have
#   been tested in lab situations, all use cases cannot be accounted for.
# Usage example:
#   python repl_lag.py -m 192.168.0.105 -u admin -p Netapp1!
# Output example:
#   Volume ID: 1
#   Volume name: LinuxVol1
#   Current lag: 00:00:00.000000
#
#
#   Volume ID: 2
#   Volume name: LinuxVol2
#   Current lag: 00:00:00.000000
"""

import json
from modules.build_auth import build_auth
from modules.choose_inputs import get_inputs_default as get_inputs
from modules.connect_cluster import connect_cluster_rest as connect_cluster

def build_payload():
    """
    Get list of replicated volumes and query lag
    return that for connect_cluster to gather data
    """
    payload = json.dumps({"method": "ListActivePairedVolumes",
                          "params": {}, "id": 1})
    return payload


def get_replication_status(response_json):
    """
    Create a dictionary of the replicated volumes on the cluster
    This is used to ensure we can track volume ID to volume name from
    disparate data sources that don't all contain both sets of data
    """
    paired_vols = {}
    for volume in response_json['result']['volumes']:
        vol_id = volume['volumeID']
        vol_name = volume['name']
        paired_vols[vol_id] = vol_name
    return paired_vols


def get_vol_stats(paired_vols):
    """
    Build the list of volumes to pull the lag time from
    return it for parse_volume_stats
    """
    vol_list = []
    for vol_id, _vol_name in paired_vols.items():
        vol_list.append(vol_id)
    payload = json.dumps({"method": "ListVolumeStats",
                          "params": {"volumeIDs": vol_list},
                          "id": 1})
    return payload


def parse_volume_stats(paired_vols, response_json):
    """
    Display the volume ID, name, and lag for the customer
    You can return data from here to another function for alerting if desired
    That alerting function is not included
    """
    for vol_id, name in paired_vols.items():
        for volume in response_json['result']['volumeStats']:
            if volume['volumeID'] == vol_id:
                print("Volume ID: {}\nVolume name: {}"
                      "\nCurrent lag: {}"
                      "\n\n".format(vol_id, name, volume['asyncDelay']))


def main():
    """
    Calling everything above here to get an output
    """
    mvip, user, user_pass, mvip_node = get_inputs()
    payload = build_payload()
    headers, url = build_auth(mvip, user, user_pass, mvip_node)
    response_json = connect_cluster(headers, url, payload)
    paired_vols = get_replication_status(response_json)
    payload = get_vol_stats(paired_vols)
    response_json = connect_cluster(headers, url, payload)
    parse_volume_stats(paired_vols, response_json)


if __name__ == "__main__":
    main()
