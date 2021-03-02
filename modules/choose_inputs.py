#!/usr/bin/python
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.4 and above
# No warranty is offered, use at your own risk.  While these scripts have
#   been tested in lab situations, all use cases cannot be accounted for.
"""

import argparse
from getpass import getpass


def get_inputs_api():
    """
    Get user inputs for what to connect to and what credentials to use
        and what API call to run
    -m mvip
    -a api
    -u user
    -p user_pass
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str,
                        required=True,
                        metavar='mvip',
                        help='MVIP/node name or IP')
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='user',
                        help='username to connect with')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='password for user')
    parser.add_argument('-a', type=str,
                        required=False,
                        metavar='api',
                        help='API call to run')
    parser.add_argument('-v',
                        action='store_true')
    parser.add_argument('-f',
                        action='store_true')
    parser.add_argument('-x', type=str,
                        required=False,
                        metavar='extra_params',
                        help='Extra parameters required for API')
    args = parser.parse_args()

    mvip = args.m
    user = args.u
    if not args.p:
        user_pass = getpass("Enter password for user: {} "
                            "on cluster {}: ".format(user,
                                                     mvip))
    else:
        user_pass = args.p

    if args.a is not None:
        api = args.a
    if args.x is not None:
        param1 = (args.x).split(",")[0]
        param2 = (args.x).split(",")[1]
    else:
        param1 = '"force"'
        param2 = '"True"'

    return mvip, user, user_pass, api, param1, param2


def get_inputs_node():
    """
    Used to connect to nodes
    -n node
    -u user
    -p user_pass
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=str,
                        required=True,
                        metavar='node',
                        help='node name or IP')
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='user',
                        help='username to connect with')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='password for user')
    args = parser.parse_args()

    node = args.n
    user = args.u

    if not args.p:
        user_pass = getpass("Enter password for user {} "
                            "on cluster {}: ".format(user,
                                                     node))
    else:
        user_pass = args.p
    return node, user, user_pass


def get_inputs_vol_naa_id():
    """
    Get inputs
    -m mvip
    -u user
    -p user_pass
    -i vol_id
    -s naa_id
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str,
                        required=True,
                        metavar='mvip',
                        help='MVIP/node name or IP')
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='user',
                        help='username to connect with')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='password for user')
    parser.add_argument('-i', type=int,
                        required=False,
                        metavar='vol_id',
                        help='vol id to search on')
    parser.add_argument('-s', type=str,
                        required=False,
                        metavar='naa_id',
                        help='naaid to search on')
    parser.add_argument('--sessions',
                        action='store_true',
                        help='Set if you want to see iSCSI sessions ' \
                        'associated with this volme')
    args = parser.parse_args()

    mvip = args.m
    user = args.u
    naa_id = args.s
    vol_id = args.i
    sessions = args.sessions
    if not args.p:
        user_pass = getpass("Enter password for user {} "
                            "on cluster {}: ".format(user,
                                                     mvip))
    else:
        user_pass = args.p

    return mvip, user, user_pass, naa_id, vol_id, sessions


def get_inputs_search_id():
    """
    Get inputs
    -m mvip
    -u user
    -p user_pass
    -i search_id
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str,
                        required=True,
                        metavar='mvip',
                        help='MVIP/node name or IP')
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='user',
                        help='username to connect with')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='password for user')
    parser.add_argument('-i', type=str,
                        required=False,
                        metavar='search_id',
                        help='input an id to search for')
    parser.add_argument('--connect', choices=['cluster', 'node'],
                        required=False,
                        metavar='mvip_node',
                        help='should we connect to a cluster or node')
    args = parser.parse_args()

    mvip = args.m
    user = args.u
    search_id = args.i
    mvip_node = args.connect
    if not args.p:
        user_pass = getpass("Enter password for user {} "
                            "on cluster {}: ".format(user,
                                                     mvip))
    else:
        user_pass = args.p

    return mvip, user, user_pass, mvip_node, search_id


def get_inputs_node_id_or_name():
    """
    This function is for gather node ID or name
    may be deprecated in future releases
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str,
                        required=True,
                        metavar='mvip',
                        help='MVIP/node name or IP')
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='username',
                        help='username to connect with')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='password for user')
    parser.add_argument('-i', type=int,
                        required=False,
                        metavar='node_id',
                        help='nodeID to gather from')
    parser.add_argument('-n', type=str,
                        required=False,
                        metavar='node_name',
                        help='nodeID to gather from')
    args = parser.parse_args()

    mvip = args.m
    user = args.u
    if args.i is not None:
        node_id = args.i
    else:
        node_id = None
    if args.n is not None:
        node_name = args.n
    else:
        node_name = None
    if not args.p:
        user_pass = getpass("Enter password for user {} "
                            "on cluster {}: ".format(user,
                                                     mvip))
    else:
        user_pass = args.p
    return mvip, user, user_pass, node_id, node_name


def get_inputs_service_info():
    """
    This function is for getting the slice service info
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str,
                        required=True,
                        metavar='mvip',
                        help='MVIP/node name or IP')
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='username',
                        help='username to connect with')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='password',
                        help='password for user')
    parser.add_argument('-i', type=int,
                        required=False,
                        metavar='acct_id',
                        help='account id to filter on')
    parser.add_argument('-a', type=str,
                        required=False,
                        metavar='acct_name',
                        help='account name to look up')
    parser.add_argument('-e', type=bool,
                        required=False,
                        default=False,
                        metavar='all_vols',
                        help='check all volumes')
    args = parser.parse_args()

    mvip = args.m
    user = args.u
    acct_id = args.i
    acct_name = args.a
    all_vols = args.e
    if acct_name is None and acct_id is None:
        all_vols = True
    if not args.p:
        user_pass = getpass("Enter password for user {} "
                            "on cluster {}: ".format(user,
                                                     mvip))
    else:
        user_pass = args.p
    return mvip, user, user_pass, acct_id, acct_name, all_vols


def get_inputs_repl_cluster_or_vol():
    """
    This input is for clusters that have replication
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str,
                        required=True,
                        metavar='mvip',
                        help='MVIP/node name or IP')
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='user',
                        help='username to connect with')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='password for user')
    parser.add_argument('-o', type=str,
                        required=False,
                        metavar='check_opt',
                        choices=['cluster', 'volume'],
                        help='option for cluster or volume')
    args = parser.parse_args()

    mvip = args.m
    user = args.u
    check_opt = args.o
    if not args.p:
        user_pass = getpass("Enter password for user {} "
                            "on cluster {}: ".format(user,
                                                     mvip))
    else:
        user_pass = args.p

    return mvip, user, user_pass, check_opt


def get_inputs_default():
    """
    Basic get user inputs for what to connect to and what credentials to use
    -m mvip
    -u user
    -p user_pass
    --connect mvip or node level run
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str,
                        required=True,
                        metavar='mvip',
                        help='MVIP/node name or IP')
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='user',
                        help='username to connect with')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='password for user')
    parser.add_argument('--connect', choices=['cluster', 'node'],
                        required=False,
                        metavar='mvip_node',
                        help='should we connect to a cluster or node')
    args = parser.parse_args()

    mvip = args.m
    user = args.u
    mvip_node = args.connect
    if not args.p:
        user_pass = getpass("Enter password for user: {} "
                            "on cluster {}: ".format(user,
                                                     mvip))
    else:
        user_pass = args.p

    return mvip, user, user_pass, mvip_node


def get_inputs_default_force():
    """
    Basic get user inputs for what to connect to and what credentials to use
    -m mvip
    -u user
    -p user_pass
    --connect mvip or node level run
    --force force a reset
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str,
                        required=True,
                        metavar='mvip',
                        help='MVIP/node name or IP')
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='user',
                        help='username to connect with')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='password for user')
    parser.add_argument('--connect', choices=['cluster', 'node'],
                        required=False,
                        metavar='mvip_node',
                        help='should we connect to a cluster or node')
    parser.add_argument('--force-reset',
                        dest='force_reset',
                        default=False,
                        action='store_true')
    args = parser.parse_args()

    mvip = args.m
    user = args.u
    mvip_node = args.connect
    if not args.p:
        user_pass = getpass("Enter password for user: {} "
                            "on cluster {}: ".format(user,
                                                     mvip))
    else:
        user_pass = args.p
    
    force_reset = args.force_reset

    return mvip, user, user_pass, mvip_node, force_reset


def get_inputs_ssh():
    """
    Basic get user inputs for what to connect to and what credentials to use
    -m mvip
    -u user
    -p user_pass
    --connect mvip or node level run
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str,
                        required=True,
                        metavar='mvip',
                        help='MVIP/node name or IP')
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='user',
                        help='username to connect with')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='password for user')
    parser.add_argument('--connect', choices=['cluster', 'node'],
                        required=False,
                        metavar='mvip_node',
                        help='should we connect to a cluster or node')
    parser.add_argument('--ssh-state', choices=['enable', 'disable'],
                        required=True,
                        metavar='ssh_state',
                        dest='ssh_state',
                        help='enable or disable SSH')
    parser.add_argument('--duration', type=str,
                        required=False,
                        metavar='duration',
                        help='duration to enable SSH if cluster')
    args = parser.parse_args()

    mvip = args.m
    user = args.u
    mvip_node = args.connect
    ssh_state = args.ssh_state
    duration = args.duration

    if not args.p:
        user_pass = getpass("Enter password for user: {} "
                            "on cluster {}: ".format(user,
                                                     mvip))
    else:
        user_pass = args.p

    return mvip, user, user_pass, mvip_node, duration, ssh_state


def get_inputs_rtfi():
    """
    Basic get user inputs for what to connect to and what credentials to use
    -m mvip
    -u user
    -p user_pass
    --build local to reset node to current version
    --build remote to update to a new image
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str,
                        required=True,
                        metavar='mvip',
                        help='MVIP/node name or IP')
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='user',
                        help='username to connect with')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='password for user')
    parser.add_argument('--build', choices=['local', 'remote'],
                        required=True,
                        metavar='build',
                        help='should we connect to a local or remote image')
    args = parser.parse_args()

    mvip = args.m
    user = args.u
    build = args.build
    if not args.p:
        user_pass = getpass("Enter password for user: {} "
                            "on cluster {}: ".format(user,
                                                     mvip))
    else:
        user_pass = args.p

    return mvip, user, user_pass, build


def get_inputs_create_vol():
    """
    Basic get user inputs for what to connect to and what credentials to use
    -m mvip
    -u user
    -p user_pass
    --connect mvip or node level run
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str,
                        required=True,
                        metavar='mvip',
                        help='MVIP/node name or IP')
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='user',
                        help='username to connect with')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='password for user')
    parser.add_argument('--connect', choices=['cluster', 'node'],
                        required=False,
                        metavar='mvip_node',
                        help='should we connect to a cluster or node')
    parser.add_argument('--vol-name', type=str,
                        required=True,
                        metavar='vol_name',
                        help='name of volume to create')
    parser.add_argument('--acct-id', type=int,
                        required=True,
                        metavar='acct_id',
                        help='account to associate volume with')
    parser.add_argument('--enable-512e',
                        choices=['enable', 'disable'],
                        required=True,
                        metavar='en_512',
                        help='set 512 byte emulation')
    parser.add_argument('--qos-tier',
                        choices=['silver', 'gold', 'plat'],
                        required=True,
                        metavar='qos_tier',
                        help='name of volume to create')
    parser.add_argument('--vol-size',
                        choices=['1T','2T','3T','4T','5T','6T','7T','8T',
                                 '16g','32g','64g','128g','256g','512g'],
                        metavar='vol_size',
                        help='size of volume to create')
    parser.add_argument('--vol-access-group', type=str,
                        required=False,
                        dest="vol_acc_grp",
                        metavar='vol_acc_grp',
                        help='volume group to assign to')
    args = parser.parse_args()

    mvip = args.m
    user = args.u
    mvip_node = args.connect
    if not args.p:
        user_pass = getpass("Enter password for user: {} "
                            "on cluster {}: ".format(user,
                                                     mvip))
    else:
        user_pass = args.p
    vol_name = args.vol_name
    acct_id = args.acct_id
    en_512 = args.enable_512e
    qos_tier = args.qos_tier
    vol_size = args.vol_size
    vol_acc_grp = args.vol_acc_grp


    return (mvip, user, user_pass, mvip_node, vol_name,
            acct_id, en_512, qos_tier, vol_size, vol_acc_grp)
