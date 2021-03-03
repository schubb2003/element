#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.7 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""

import sys
import time
import os
import json
from datetime import datetime
from prettytable import PrettyTable
from modules.choose_inputs import get_inputs_default as get_inputs
from modules.build_auth import build_auth
from modules.connect_cluster import connect_cluster_rest as connect_cluster


def build_cluster_events():
    fault_payload = json.dumps({"method": "ListClusterFaults",
                                "params": {"faultTypes": "current",
                                           "bestPractices": False},
                                "id": 1})
    return fault_payload


def parse_events(response_json):
    """
    Build the events list
    """
    fault_dict = {}
    for res_out in response_json['result']['faults']:
        if res_out['resolved'] is False:
            flt_details = res_out['details']
            flt_node = res_out['nodeID']
            flt_drive = res_out['driveID']
            flt_svc = res_out['serviceID']
            flt_date = res_out['date']
            flt_type = res_out['type']
            flt_sev = res_out['severity']
            flt_key = res_out['clusterFaultID']
            fault_dict[flt_key] = [flt_node, flt_drive,
                                   flt_svc, flt_date, flt_type,
                                   flt_sev, flt_details]
    if len(fault_dict) == 0:
        print(f"No events found")
    return fault_dict


def print_table(outfile_name, fault_dict):
    flt_table = PrettyTable()
    flt_table.field_names = ["Node ID", "Drive ID", "Service ID",
                             "Date", "Type", "Severity", "Details"]
    # flt_table.max_width['Details'] = 60
    for val in fault_dict.values():
        flt_table.add_row([*val])
    print(flt_table.get_string(sortby="Severity"))
    flt_table_text = flt_table.get_string()
    with open("./output_files/" + outfile_name, "a") as out_file:
        out_file.write(flt_table_text + "\n")


def get_filename(mvip):
    """
    Build the output filename
    """
    now_date = datetime.now()
    out_date = now_date.strftime("%Y-%m-%d_%H-%M")
    outfile_name = mvip + "_cluster_faults_" + out_date + '.txt'
    if os.path.exists(outfile_name):
        os.remove(outfile_name)
    print('Output file name is: {}'.format(outfile_name))
    return outfile_name


def main():
    """
    Do the work
    """
    mvip, user, user_pass, mvip_node = get_inputs()
    fault_payload = build_cluster_events()
    headers, url = build_auth(mvip, user, user_pass, mvip_node)
    response_json = connect_cluster(headers, url, fault_payload)
    fault_dict = parse_events(response_json)
    outfile_name = get_filename(mvip)
    print_table(outfile_name, fault_dict)


if __name__ == "__main__":
    main()
