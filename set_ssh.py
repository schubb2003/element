#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.6 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
#########18-may-2020
# Need to address when cluster or node is selected, but user has input the
#   opposite connection type.
#########
"""

import json
from datetime import datetime, timedelta
from modules.choose_inputs import get_inputs_ssh as get_inputs
from modules.build_auth import build_auth
from modules.connect_cluster import connect_cluster_rest as connect_cluster


def build_payload(mvip_node, ssh_state, duration_set=None):
    """
    Build the API call to enable SSH on an 11.3 or higher cluster
    """
    ssh_command = ssh_state.capitalize()

    if duration_set is None:
        duration_set = "02:00:00"

    if mvip_node == "cluster":
        ssh_method = ssh_command + "ClusterSsh"
        payload = json.dumps({"method": ssh_method,
                              "params": {"duration": duration_set}, "id": 1})
        return payload

    elif mvip_node == "node":
        ssh_method = ssh_command + "Ssh"
        payload = json.dumps({"method": ssh_method,
                              "params": {}, "id": 1})
        return payload
    else:
        print("Expected cluster/node input of:\t{}".format(mvip_node))


def set_ssh_state(ssh_state, mvip_node, duration_set: None):
    """
    Set the SSH state as requested by the user
    """
    if ssh_state == "enable":
        if duration_set is None:
            duration_set = "02:00:00"

        right_now = datetime.now()
        search_hour = duration_set.split(":")[0]
        search_minute = duration_set.split(":")[1]
        duration_time = (int(search_hour)*60) + int(search_minute)
        time_delta = timedelta(minutes=duration_time)
        end_time = (right_now + time_delta)
        end_time_out = end_time.isoformat()

    if ssh_state == "enable":
        if mvip_node == "cluster":
            print("\nSSH has been enabled "
                  "until\t{} local time".format(end_time_out))
        else:
            print("\nSSH has been enabled")
    else:
        print("\nSSH has been disabled")


def main():
    """
    Do the work
    """
    mvip, user, user_pass, mvip_node, duration_set, ssh_state = get_inputs()
    headers, url = build_auth(mvip, user, user_pass, mvip_node)
    payload = build_payload(mvip_node, ssh_state, duration_set)
    connect_cluster(headers, url, payload)
    set_ssh_state(ssh_state, mvip_node, duration_set)

if __name__ == "__main__":
    main()
