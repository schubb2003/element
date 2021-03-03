#!/usr/bin/python3
"""
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.6 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
"""

import sys
from prettytable import PrettyTable


def build_table_dual_column_dict(hdr1, hdr2, out_dict):
    """
    Builds the table outputs and writes them to a file
    """
    out_tbl = PrettyTable()
    out_tbl.field_names = (hdr1, hdr2)
    out_tbl.align[hdr1] = 'l'
    out_tbl.align[hdr2] = 'l'
    for key, value in out_dict.items():
        out_tbl.add_row([key, value])
    print(f"{out_tbl}\n\n")


def build_table_triple_column_dict(hdr1, hdr2, hdr3, out_dict):
    """
    Builds the table outputs and writes them to a file
    """
    out_tbl = PrettyTable()
    out_tbl.field_names = (hdr1, hdr2, hdr3)
    out_tbl.align[hdr1] = 'l'
    out_tbl.align[hdr2] = 'l'
    out_tbl.align[hdr3] = 'l'
    for key, value in out_dict.items():
        out_tbl.add_row([key, value[1], value[2]])
    print(f"{out_tbl}\n\n")


def autosized_table_one_row(hdr_list, data_in):
    """
    pass headers and values as a list and the
      system will auto create the table size.
    Note this is single row only
    """
    out_tbl = PrettyTable()
    out_tbl.field_names = (hdr_list)
    for hdr in hdr_list:
        out_tbl.align[hdr] = 'l'
    if type(data_in) == dict:
        for vals in data_in.values():
            out_tbl.add_row([*vals])
    elif type(data_in) == tuple:
        out_tbl.add_row([*data_in])
    else:
        print(f"Unexpected data type in, exiting")
        sys.exit(1)
    print(f"{out_tbl}\n\n")


def autosized_table_two_rows(hdr_list, list_one, list_two):
    """
    pass headers and values as a list and the
      system will auto create the table size.
    Note this supports two rows
    """
    out_tbl = PrettyTable()
    out_tbl.field_names = (hdr_list)
    for hdr in hdr_list:
        out_tbl.align[hdr] = 'l'
    out_tbl.add_row([*list_one])
    out_tbl.add_row([*list_two])
    print(f"{out_tbl}\n\n")


def autosized_table(hdr_list, lists):
    """
    pass headers and a list of lists as a list
      and the system will auto create the table size
    """
    out_tbl = PrettyTable()
    out_tbl.field_names = (hdr_list)
    for hdr in hdr_list:
        out_tbl.align[hdr] = 'l'
    for list in lists:
        out_tbl.add_row([*list])
    print(f"{out_tbl}\n\n")


def autosized_table_two_column(data_in):
    """
    pass headers and values as a list and the system
      will auto create the table size. Note this is single row only
    """
    out_tbl = PrettyTable()
    out_tbl.field_names = ("API out", "Response")
    out_tbl.align["API out"] = "l"
    out_tbl.align["Response"] = "l"
    for data_key, data_val in data_in.items():
        out_tbl.add_row([data_key, data_val])
    print(f"{out_tbl}\n\n")


def main():
    """
    Nothing happens here
    """
    print("This is a module designed to handle building "
          "auth credentials to solidfire clusters, exiting.")

if __name__ == "__main__":
    main()
