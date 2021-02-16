#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.4 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""

import json
from modules.choose_inputs import get_inputs_default as get_inputs
from modules.build_auth import build_auth
from modules.connect_cluster import connect_cluster_rest as connect_cluster


def build_payload():
    """
    Build the payload for the API
    """
    payload = json.dumps({"method": "GetLldpInfo", "params":{}, "id": 1})
    return payload


def get_switch_info(response_json):
    """
    Call the LLDP API to get switch info
    """
    #print(json.dumps(response_json, sort_keys=True, indent=4))
    lldp_loads = response_json
    for net_interface in (lldp_loads['result']
                          ['lldpInfo']
                          ['lldpNeighbors']
                          ['lldp']):
        for interfaces in net_interface['interface']:
            for chassis_out in interfaces['chassis']:
                chassis_type = chassis_out['descr']
                for item in chassis_type:
                    item_descr = item['value'].replace('\n', ' ')
                chassis_ip = chassis_out['mgmt-ip']
                for item in chassis_ip:
                    item_ip = item['value']
                chassis_id = chassis_out['id']
                for item in chassis_id:
                    item_model = item['value']
                chassis_name = chassis_out['name']
                for item in chassis_name:
                    item_name = item['value']
            for vlan in interfaces['vlan']:
                vlan_id = vlan['vlan-id']
            print("\nChassis description:\t{}"
                  "\nChassis IP:\t\t{}"
                  "\nChassis name:\t\t{}"
                  "\nVLAN ID:\t\t{}\n\n".format(item_descr,
                                                item_ip,
                                                item_name,
                                                vlan_id))


def get_cluster_info(response_json):
    """
    Get the cluster information
    """
    #print(json.dumps(response_json, sort_keys=True, indent=4))
    vlan_list = []
    lldp_loads = response_json
    for net_interface in (lldp_loads['result']
                          ['lldpInfo']
                          ['lldpInterfaces']
                          ['lldp']):
        for vlan_interface in net_interface['interface']:
            for chassis_out in vlan_interface['chassis']:
                for name_out in chassis_out['name']:
                    node_name = name_out['value']
            for key in vlan_interface.keys():
                if key == 'vlan':
                    for vlan in vlan_interface['vlan']:
                        vlan_list.append(vlan['vlan-id'])
                else:
                    pass
        vlan_list = set(vlan_list)
        print("Node {} VLAN configuration".format(node_name))
        for vlan in vlan_list:
            print("VLAN {} configured on node.".format(vlan))


def main():
    """
    Call the functions from above
    """
    mvip, user, user_pass = get_inputs()
    headers, url = build_auth(mvip, user, user_pass)
    payload = build_payload()
    response_json = connect_cluster(headers, url, payload)
    get_switch_info(response_json)
    get_cluster_info(response_json)


if __name__ == "__main__":
    main()
