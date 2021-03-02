get_cluster_stats.py
	This basic script will pull clusters utilization stats
	
c:\Git\element-test-branch>python get_cluster_stats.py -m solidfire-test -u admin -p solidfire
Enter password for user: admin on cluster solidfire-test
+----------------------------+-----------------------------+
| API out                    | Response                    |
+----------------------------+-----------------------------+
| Actual IOPS                | 0                           |
| Average IO Size            | 0                           |
| Client Queue Depth         | 0                           |
| Cluster Utilization        | 0.0                         |
| Latency in Usec            | 0                           |
| Normalized IOPS            | 0                           |
| Read Bytes                 | 302628352                   |
| Read Bytes in Last Sample  | 0                           |
| Read Usec                  | 0                           |
| Read Usec Total            | 0                           |
| Read Ops                   | 6191                        |
| Read Ops in Last Sample    | 0                           |
| Timestamp                  | 2021-03-02T16:16:52.545034Z |
| Unaligned Reads            | 2167                        |
| Unaligned Writes           | 363                         |
| Write Bytes                | 5822052864                  |
| Write Bytes in Last Sample | 0                           |
| Write Usec                 | 0                           |
| Write Usec Total           | 0                           |
| Write Ops                  | 27469                       |
| Write Ops in Last Sample   | 0                           |
+----------------------------+-----------------------------+

get_iscsi_session_count.py
	This script will provide the count of iscsi sessions on each node, plus the overall session count
c:\Git\element-test-branch>python get_iscsi_session_count.py -m solidfire-test -u admin
Enter password for user: admin on cluster solidfire-test:
Using token authentication
+-------------+---------------------+
| Node Name   | iSCSI session count |
+-------------+---------------------+
| TestNode02  | 2                   |
| TestNode03  | 1                   |
| TestNode01  | 2                   |
| TestNode04  | 1                   |
+-------------+---------------------+	
	
get_iscsi_sessions.py
	This script will provide the actual connection information:
		Session ID, Node ID, Node Name, Volume ID, Volume Name, Initiator Name, Target Name
		You can search on a string and it will return exact matches only
		You can search on things such as node/vol ID, however please note they will return ANY match so vol ID 13 will return as well as node ID 13
c:\Git\element-test-branch>python get_iscsi_sessions.py -m solidfire-test -u admin
Enter password for user admin on cluster solidfire-test:
Using token authentication
+--------------+---------+-------------+-----------+-----------------------------+---------------------------------------+--------------------------------+
| Session ID   | Node ID | Node Name   | Volume ID | Volume Name                 | Initiator                             | Target Host                    |
+--------------+---------+-------------+-----------+-----------------------------+---------------------------------------+--------------------------------+
| 47246006168  | 2       |  TestNode02 | 13        | rcl-sqltest-snap23-c7b001b3 | iqn.1991-05.com.microsoft:rcl-sqltest | iqn.2010-01.com.solidfire:p1gn |
| 47246006171  | 2       |  TestNode02 | 3         | vsstest003                  | iqn.1991-05.com.microsoft:rcl-sqltest | iqn.2010-01.com.solidfire:p1gn |
| 81608628129  | 3       |  TestNode03 | 1         | vsstest001                  | iqn.1991-05.com.microsoft:rcl-sqltest | iqn.2010-01.com.solidfire:p1gn |
| 253403071472 | 1       |  TestNode01 | 15        | rcl-sqltest-snap24-c7b001b3 | iqn.1991-05.com.microsoft:rcl-sqltest | iqn.2010-01.com.solidfire:p1gn |
| 253403071473 | 1       |  TestNode01 | 14        | rcl-sqltest-snap25-c7b001b3 | iqn.1991-05.com.microsoft:rcl-sqltest | iqn.2010-01.com.solidfire:p1gn |
| 274877907950 | 5       |  TestNode04 | 2         | vsstest002                  | iqn.1991-05.com.microsoft:rcl-sqltest | iqn.2010-01.com.solidfire:p1gn |
+--------------+---------+-------------+-----------+-----------------------------+---------------------------------------+--------------------------------+

c:\Git\element-test-branch>python get_iscsi_sessions.py -m solidfire-test -u admin -i vsstest003
Enter password for user admin on cluster solidfire-test:
Using token authentication
+-------------+---------+-------------+-----------+-------------+---------------------------------------+--------------------------------+
| Session ID  | Node ID | Node Name   | Volume ID | Volume Name | Initiator                             | Target Host                    |
+-------------+---------+-------------+-----------+-------------+---------------------------------------+--------------------------------+
| 47246006171 | 2       |  TestNode02 | 3         | vsstest003  | iqn.1991-05.com.microsoft:rcl-sqltest | iqn.2010-01.com.solidfire:p1gn |
+-------------+---------+-------------+-----------+-------------+---------------------------------------+--------------------------------+



c:\Git\element-test-branch>python get_iscsi_sessions.py -m solidfire-test -u admin -i  TestNode02
Enter password for user admin on cluster solidfire-test:
Using token authentication
+-------------+---------+-------------+-----------+-----------------------------+---------------------------------------+--------------------------------+
| Session ID  | Node ID | Node Name   | Volume ID | Volume Name                 | Initiator                             | Target Host                    |
+-------------+---------+-------------+-----------+-----------------------------+---------------------------------------+--------------------------------+
| 47246006168 | 2       |  TestNode02 | 13        | rcl-sqltest-snap23-c7b001b3 | iqn.1991-05.com.microsoft:rcl-sqltest | iqn.2010-01.com.solidfire:p1gn |
| 47246006171 | 2       |  TestNode02 | 3         | vsstest003                  | iqn.1991-05.com.microsoft:rcl-sqltest | iqn.2010-01.com.solidfire:p1gn |
+-------------+---------+-------------+-----------+-----------------------------+---------------------------------------+--------------------------------+



c:\Git\element-test-branch>python get_iscsi_sessions.py -m solidfire-test -u admin -i iqn.1991-05.com.microsoft:rcl-sqltest
Enter password for user admin on cluster solidfire-test:
Using token authentication
+--------------+---------+-------------+-----------+-----------------------------+---------------------------------------+--------------------------------+
| Session ID   | Node ID | Node Name   | Volume ID | Volume Name                 | Initiator                             | Target Host                    |
+--------------+---------+-------------+-----------+-----------------------------+---------------------------------------+--------------------------------+
| 47246006168  | 2       |  TestNode02 | 13        | rcl-sqltest-snap23-c7b001b3 | iqn.1991-05.com.microsoft:rcl-sqltest | iqn.2010-01.com.solidfire:p1gn |
| 47246006171  | 2       |  TestNode02 | 3         | vsstest003                  | iqn.1991-05.com.microsoft:rcl-sqltest | iqn.2010-01.com.solidfire:p1gn |
| 81608628129  | 3       |  TestNode03 | 1         | vsstest001                  | iqn.1991-05.com.microsoft:rcl-sqltest | iqn.2010-01.com.solidfire:p1gn |
| 253403071472 | 1       |  TestNode01 | 15        | rcl-sqltest-snap24-c7b001b3 | iqn.1991-05.com.microsoft:rcl-sqltest | iqn.2010-01.com.solidfire:p1gn |
| 253403071473 | 1       |  TestNode01 | 14        | rcl-sqltest-snap25-c7b001b3 | iqn.1991-05.com.microsoft:rcl-sqltest | iqn.2010-01.com.solidfire:p1gn |
| 274877907950 | 5       |  TestNode04 | 2         | vsstest002                  | iqn.1991-05.com.microsoft:rcl-sqltest | iqn.2010-01.com.solidfire:p1gn |
+--------------+---------+-------------+-----------+-----------------------------+---------------------------------------+--------------------------------+

get_master_ensemble.py
	This script will output all of the ensemble nodes as well as the master for quick identificaiton
	
get_min_qos.py
	This script simply outputs the total sum of the set min IOPs

get_vol_primary_service_id_v2.py
	This script will outline what node a given volume is on, what nodes volumes for an account are on, or a count of how many volume primaries are on each node

irc_check_no_inv.py
	This script creates a build checklist of various configurations for configuration management, build verification, etc

list_accounts.py
	This basic script simply lists all accounts on a cluster

list_active_vols.py
	This script dumps out the information on the volumes on the cluster
		This should be seen almost as a training script
		
list_replicated_vols.py
	This script lists the replicated volumes on a given cluster

list_virt_nets.py
	This script lists out the configured VLANs

lldp2.py
	This script is a base implementation of the LLDP protocol's output
	LLDP is used to gather switch information

repl_lag.py
	This script was put together to show how to pull replication information
		It was necessary as the information is stored with the volume, not the replication information

set_qos_policy.py
	This script allows you to implement QoS policies across a cluster
	It will alert you if there are mismatches without --force-reset
