#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.4 and above
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
    payload = json.dumps({"method": "ListAccounts", "params":{}, "id": 1})
    #payload = json.dumps({"method": "ListReports","params":{},"id": 1})
    return payload


def create_table(response_json):
    """
    Build the output table
    """
    account_table = PrettyTable()
    account_table.field_names = (["Account ID", "Account Name"])
    for account in response_json['result']['accounts']:
        account_id = account['accountID']
        account_name = account['username']
        print(account_id, account_name)
        account_table.add_row([account_id, account_name])
    return account_table


def main():
    """
    Call the above functions
    """
    mvip, user, user_pass, mvip_node = get_inputs()
    headers, url = build_auth(mvip, user, user_pass, mvip_node)
    payload = build_payload()
    response_json = connect_cluster(headers, url, payload)
    account_table = create_table(response_json)
    print(account_table)


if __name__ == "__main__":
    main()
