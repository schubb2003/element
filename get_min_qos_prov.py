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
from prettytable import PrettyTable


def build_payload():
    """
    Get list of replicated volumes and query lag
    return that for connect_cluster to gather data
    """
    payload = json.dumps({"method": "ListVolumes",
                          "params": {}, "id": 1})
    return payload


def do_stuff(response_json):
    qos_min = 0
    qos_total = 0
    for vol in response_json['result']['volumes']:
        qos_min = (vol['qos']['minIOPS'])
        qos_total = qos_total + qos_min
    print(f"Total is: {qos_total}")


def main():
    mvip, user, user_pass, mvip_node = get_inputs()
    headers, url = build_auth(mvip, user, user_pass, mvip_node)
    payload = build_payload()
    response_json = connect_cluster(headers, url, payload)
    do_stuff(response_json)


if __name__ == "__main__":
    main()
