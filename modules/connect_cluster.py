#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.6 and above
# No warranty is offered, use at your own risk.  While these scripts have
#   been tested in lab situations, all use cases cannot be accounted for.
# This script connects to a cluster or node and does some basic error handling
"""

import json
import sys
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def connect_cluster_rest(headers, url, payload):
    """
    Self explanatory - this is how we connect to SolidFire cluster
    Basic error handling for standard connectivity failures
    """
    try:
        response = requests.request("POST",
                                    url,
                                    data=payload,
                                    headers=headers,
                                    verify=False)
        res_code = response.status_code
        res_text = response.text

        if res_code == 200 and '"code":500' not in res_text:
            response_json = json.loads(res_text)
            return response_json
        elif res_code == 401:
            print(f"Status {res_code}.  Access denied, "
                  f"please verify username and password")
            sys.exit(1)
        elif response.status_code == 200 and '"code":500' in res_text:
            if "xUnknownUsername" in res_text:
                print(f"Status {res_code}, but error 500.  LDAP does not "
                      f"appear to be configured, please verify.\n"
                      f"The user has been authenticated "
                      f"but not authorized for access")
                sys.exit(1)
            elif "xPermissionDenied" in res_text:
                print(f"Status {res_code}.  Access denied, "
                      f"please verify username and password")
            elif "xUnknownAPIMethod" in res_text:
                print(f"Status {res_code}, but error 500.  Unknown API "
                      f"Verify the API call is valid and "
                      f"resubmit\nResponse text is: {res_text}")
                sys.exit(res_code)
            else:
                print(f"Status {res_code}, but error returned.\n{res_text}"
                      f"verify the error and resubmit")
        elif res_code == 200 and 'null' in res_text:
            print(f"Status {res_text}, there appears to be an issue with this "
                  f"node. This can happen during an upgrade when the node "
                  f"responds to pings, but is not serving web traffic. "
                  f"Check the node health and try again")
            sys.exit(res_code)
        elif res_code == 502:
            print(f"Please check that this command is being run against "
                  f"a node or cluster as expected.\nStatus: {res_code} "
                  f" This is usually due to running a node command against "
                  f"a cluster or vice versa")
            sys.exit(res_code)
        else:
            print(f"Unexpected HTML status in connect cluster module. " 
                  f"Status code is: {res_code}.\nError message:\n{res_text}.\n"
                  f"Script will now exit")
            sys.exit(res_code)

    except requests.RequestException as my_except:
        if "Max retries exceeded" in str(my_except):
            print(f"Please verify the cluster name is "
                  f"{url} and retry, host did not respond.")
            sys.exit(1)
        else:
            str_my_except = str(my_except)
            print(f"Unhandled exception:\n{str_my_except}")


def main():
    """
    Do nothing
    """
    print(f"This is a module designed to handle connecting to "
          f"solidfire clusters, exiting.")

if __name__ == "__main__":
    main()
