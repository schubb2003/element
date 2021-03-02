#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.6 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
# This script gets the network config from a single node for a node replacment
"""

import sys
import json
from modules.choose_inputs import get_inputs_default_force as get_inputs
from modules.build_auth import build_auth
from modules.connect_cluster import connect_cluster_rest as connect_cluster

def build_payload(pol_name, min_iops, max_iops, burst_iops):
    """
    Build the data payload to set the QoS if needed
    """
    pol_payload = json.dumps({"method": "CreateQoSPolicy",
                                   "params": {
                                     "name": pol_name,
                                     "qos": {"minIOPS": min_iops,
                                             "maxIOPS": max_iops,
                                             "burstIOPS": burst_iops
                                            }
                                    }
                            })
    return pol_payload


def build_list_qos_payload():
    """
    Get a list of QoS policies so we can ignore if they already exist
    """
    list_qos_payload = json.dumps({"method": "ListQoSPolicies",
                                  "params": {}})
    return list_qos_payload


def process_actions(list_response_json, headers, url, force_reset):
    """
    If a policy does not exist on a given cluster find the right values
    defined in qos_dict and apply them
    """
    qos_dict = {}
    # This dictionary sets the tiers and min/max/burst settings
    qos_dict['tiers']={"bronze":[500,5000,10000],
                       "silver":[2000,20000,50000],
                       "gold":[5000,100000,150000]}
    # Check to see if there are no policies set
    force_reset_dict = {}
    if len(list_response_json['result']['qosPolicies']) == 0:
        print(f"No existing QoS Policies found, implementing full install")
        for qos_key, qos_val in qos_dict['tiers'].items():
            pol_name = qos_key
            min_iops = qos_val[0]
            max_iops = qos_val[1]
            burst_iops = qos_val[2]
            payload = build_payload(pol_name, min_iops, max_iops, burst_iops)
            connect_cluster(headers, url, payload)
    # If there are policies ignore them if they match names, remove that
    #   name from the dict and move on
    else:
        for policy in list_response_json['result']['qosPolicies']:
            #print(f"policy:{policy}")
            pol_name = policy['name']
            pol_id = policy['qosPolicyID']
            min_iops = qos_dict['tiers'][pol_name][0]
            max_iops = qos_dict['tiers'][pol_name][1]
            burst_iops = qos_dict['tiers'][pol_name][2]
            pol_min = policy['qos']['minIOPS']
            pol_max = policy['qos']['maxIOPS']
            pol_burst = policy['qos']['burstIOPS']
            if ((min_iops !=  pol_min or max_iops !=  pol_max 
                or burst_iops != pol_burst) and force_reset is True):
                print(f"Policy mismatch detected on {pol_name}... resetting "
                      f"as reset flag is set to True")
                print(qos_dict['tiers'][pol_name])
                modify_qos_policy(headers, url, pol_id, min_iops, max_iops, burst_iops)
            elif ((min_iops !=  pol_min or max_iops !=  pol_max 
                or burst_iops != pol_burst) and force_reset is False):
                print(f"Policy mismatch detected on {pol_name}... Leaving "
                      f"as reset flag is set to false")
            if policy['name'] in qos_dict['tiers'].keys():
                qos_dict['tiers'].pop(pol_name)
                print(f"policy found: {pol_name} with min {min_iops}, "
                      f"max {max_iops} and burst {burst_iops}")    
        for pol_name, pol_values in qos_dict['tiers'].items():
            min_iops = pol_values[0]
            max_iops = pol_values[1]
            burst_iops = pol_values[2]
            payload = build_payload(pol_name, min_iops, max_iops, burst_iops)
            connect_cluster(headers, url, payload)


def modify_qos_policy(headers, url, pol_id, min_iops, max_iops, burst_iops):
    payload = json.dumps({"method": "ModifyQoSPolicy", "params": {
                           "qosPolicyID": pol_id, "qos": {"minIOPS": min_iops,
                           "maxIOPS": max_iops, "burstIOPS": burst_iops}},
                           "id": 1})
    qos_mod_response = connect_cluster(headers, url, payload)
    print(qos_mod_response)



def main():
    mvip, user, user_pass, mvip_node, force_reset = get_inputs()
    headers,url = build_auth(mvip, user, user_pass, mvip_node)
    list_qos_payload = build_list_qos_payload()
    list_response_json = connect_cluster(headers, url, list_qos_payload)
    process_actions(list_response_json, headers, url, force_reset)

if __name__ == "__main__":
    main()
