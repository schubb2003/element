#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.6 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""

import json
from modules.connect_cluster import connect_cluster_rest as connect_cluster
from modules.choose_inputs import get_inputs_default as get_inputs
from modules.build_auth import build_auth
from modules.build_table import autosized_table as build_table


def build_virt_net_payload():
    """
    Build payload
    """
    payload = json.dumps({"method": "ListVirtualNetworks",
                          "params": {}, "id": 1})
    return payload


def get_virt_net(response_json):
    """
    Get the list of virtual networks
    deadnets is used as a var name simply because they are best practice
    """
    vnet_list = []
    virt_net_list = []
    virt_nets = response_json['result']['virtualNetworks']
    for virt_net in virt_nets:
        if virt_net['attributes'] is not None:
            vnet_descript = virt_net['attributes']['description']
        else:
            vnet_descript = "No description found"
        vnet_gateway = virt_net['gateway']
        vnet_name = virt_net['name']
        vnet_mask = virt_net['netmask']
        vnet_svip = virt_net['svip']
        vnet_vlan_tag = virt_net['virtualNetworkTag']
        vnet_vlan_id = virt_net['virtualNetworkID']
        for vnet_blocks in virt_net['addressBlocks']:
            vnet_size = vnet_blocks['size']
            vnet_avail = vnet_blocks['available']
            vnet_list = [str(vnet_vlan_id), vnet_name,
                         str(vnet_vlan_tag), vnet_descript,
                         vnet_svip, vnet_mask, vnet_gateway,
                         str(vnet_size), str(vnet_avail)]
            virt_net_list.append(vnet_list)
    tbl_headers = ["VLAN ID", "Name", "VLAN Tag", "Description", "SVIP",
                   "Netmask", "Gateway", "Size", "Available"]
    return tbl_headers, virt_net_list


def main():
    """
    Do the work
    """
    mvip, user, user_pass, mvip_node = get_inputs()
    headers, url = build_auth(mvip, user, user_pass, mvip_node)
    payload = build_virt_net_payload()
    response_json = connect_cluster(headers, url, payload)
    tbl_headers, virt_net_list = get_virt_net(response_json)
    build_table(tbl_headers, virt_net_list)

if __name__ == "__main__":
    main()
