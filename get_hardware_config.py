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


def build_payload():
    """
    Build the payload for the API
    """
    hw_config_payload = json.dumps({"method": "GetHardwareConfig",
                                    "params": {"force": True}, "id": 1})

    return hw_config_payload


def parse_hw_config(hw_config_response):
    print(hw_config_response)


def main():
    mvip, user, user_pass, mvip_node = get_inputs()
    headers, url = build_auth(mvip, user, user_pass, mvip_node)
    hw_config_payload = build_payload()
    hw_config_response = connect_cluster(headers, url, hw_config_payload)
    parse_hw_config(hw_config_response)

if __name__ == "__main__":
    main()
