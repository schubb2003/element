#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.4 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""

import json
from modules.connect_cluster import connect_cluster_rest as connect_cluster
from modules.choose_inputs import get_inputs_default as get_inputs
from modules.build_auth import build_auth

def build_virt_net_payload():
    """
    Build payload
    """
    payload = json.dumps({"method": "ListVirtualNetworks",
                          "params": {},
                          "id": "1",
                         })
    return payload


def get_virt_net(response_json):
    """
    Get the list of virtual networks
    deadnets is used as a var name simply because they are best practice
    """
    return response_json

def main():
    """
    Do the work
    """
    mvip, user, user_pass, mvip_node = get_inputs()
    headers, url = build_auth(mvip, user, user_pass, mvip_node)
    payload = build_virt_net_payload()
    response_json = connect_cluster(headers, url, payload)
    get_virt_net(response_json)

if __name__ == "__main__":
    main()
