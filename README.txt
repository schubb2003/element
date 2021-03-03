get_cluster_stats.py
	This basic script will pull clusters utilization stats
-----------------------------------------------------------------------------------------------------------------------------------------
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
-----------------------------------------------------------------------------------------------------------------------------------------
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
		You can search on things such as vol ID, extensive testing has not been completed to ensure it won't ever return node ID matches as well
-----------------------------------------------------------------------------------------------------------------------------------------
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


*********MAY OR MAY NOT WORK AS EXPECTED*********
*********USE WITH CAUTION AT YOUR OWN RISK*********
c:\Git\element-test-branch>python get_iscsi_sessions.py -m solidfire-test -u admin -i 3 -p solidfire
Using token authentication
+-------------+---------+-------------+-----------+-------------+---------------------------------------+--------------------------------+
| Session ID  | Node ID | Node Name   | Volume ID | Volume Name | Initiator                             | Target Host                    |
+-------------+---------+-------------+-----------+-------------+---------------------------------------+--------------------------------+
| 47246006171 | 2       |  TestNode02 | 3         | vsstest003  | iqn.1991-05.com.microsoft:rcl-sqltest | iqn.2010-01.com.solidfire:p1gn |
+-------------+---------+-------------+-----------+-------------+---------------------------------------+--------------------------------+

get_master_ensemble.py
	This script will output all of the ensemble nodes as well as the master for quick identificaiton
-----------------------------------------------------------------------------------------------------------------------------------------
c:\Git\element-test-branch>python get_master_ensemble.py -m solidfire-test -u admin
Enter password for user: admin on cluster solidfire-test:
Using token authentication
+------------+----------------------------+
|           1|                  TestNode01|
|           2|                  TestNode02|
|      Master|                  TestNode03|
|           3|                  TestNode03|
+------------+----------------------------+

get_min_qos_prov.py
	This script simply outputs the total sum of the set min IOPs
-----------------------------------------------------------------------------------------------------------------------------------------
c:\Git\element-test-branch>python get_min_qos_prov.py -u admin -m solidfire-test
Enter password for user: admin on cluster solidfire-test:
Using token authentication
Total is: 300

get_vol_primary_service_id_v2.py
	This script will outline what node a given volume is on, what nodes volumes for an account are on, or a count of how many volume primaries are on each node
-----------------------------------------------------------------------------------------------------------------------------------------
c:\Git\element-test-branch>python get_vol_primary_service_id_v2.py -u admin -m solidfire-test -a vsstest
Enter password for user admin on cluster solidfire-test:
Using token authentication
Gathering information from: ListVolumes
Gathering information from: ListVolumeStats
Gathering information from: ListAllNodes
Gathering information from: ListServices
+-----------+-----------------------------+---------+-------------+------------+
| Volume ID |         Volume Name         | Node ID |  Node Name  | Service ID |
+-----------+-----------------------------+---------+-------------+------------+
|     1     |          VSSTest001         |    3    |  TestNode03 |     20     |
|     2     |          VSSTest002         |    5    |  TestNode04 |     65     |
|     3     |          VSSTest003         |    2    |  TestNode02 |     12     |
|     13    | RCL-SQLTest-snap23-c7b001b3 |    2    |  TestNode02 |     12     |
|     14    | RCL-SQLTest-snap25-c7b001b3 |    1    |  TestNode01 |     60     |
|     15    | RCL-SQLTest-snap24-c7b001b3 |    1    |  TestNode01 |     60     |
+-----------+-----------------------------+---------+-------------+------------+


c:\Git\element-test-branch>python get_vol_primary_service_id_v2.py -a schubb1 -m solidfire-test -u admin
Enter password for user admin on cluster solidfire-test:
Using token authentication
Gathering information from: ListVolumes
Gathering information from: ListVolumeStats
Gathering information from: ListAllNodes
Gathering information from: ListServices
Gathering information from: GetAccountByName
+-----------+---------------+---------+-------------+------------+
| Volume ID |  Volume Name  | Node ID |  Node Name  | Service ID |
+-----------+---------------+---------+-------------+------------+
|     51    |  schubb-test1 |    2    |  TestNode02 |     12     |
|     52    | schubb-test1a |    3    |  TestNode03 |     20     |
+-----------+---------------+---------+-------------+------------+


c:\Git\element-test-branch>python get_vol_primary_service_id_v2.py -m solidfire-test -u admin
Enter password for user admin on cluster solidfire-test:
Using token authentication
Gathering information from: ListVolumes
Gathering information from: ListVolumeStats
Gathering information from: ListAllNodes
Gathering information from: ListServices
+-----------+-----------------------------+---------+-------------+------------+
| Volume ID |         Volume Name         | Node ID |  Node Name  | Service ID |
+-----------+-----------------------------+---------+-------------+------------+
|     1     |          VSSTest001         |    3    |  TestNode03 |     20     |
|     2     |          VSSTest002         |    5    |  TestNode04 |     65     |
|     3     |          VSSTest003         |    2    |  TestNode02 |     12     |
|     13    | RCL-SQLTest-snap23-c7b001b3 |    2    |  TestNode02 |     12     |
|     14    | RCL-SQLTest-snap25-c7b001b3 |    1    |  TestNode01 |     60     |
|     15    | RCL-SQLTest-snap24-c7b001b3 |    1    |  TestNode01 |     60     |
|     51    |         schubb-test1        |    2    |  TestNode02 |     12     |
|     52    |        schubb-test1a        |    3    |  TestNode03 |     20     |
|     53    |         schubb-test2        |    5    |  TestNode04 |     65     |
+-----------+-----------------------------+---------+-------------+------------+
+-------------+-------------+
|  Primary ID | Slice count |
+-------------+-------------+
|  TestNode03 |      2      |
|  TestNode04 |      2      |
|  TestNode02 |      3      |
|  TestNode01 |      2      |
+-------------+-------------+


irc_check_no_inv.py
	This script creates a build checklist of various configurations for configuration management, build verification, etc

list_accounts.py
	This basic script simply lists all accounts on a cluster
-----------------------------------------------------------------------------------------------------------------------------------------
c:\Git\element-test-branch>python list_accounts.py -m solidfire-test -u admin
Enter password for user: admin on cluster solidfire-test:
Using token authentication
+------------+--------------+
| Account ID | Account Name |
+------------+--------------+
|     1      |   vsstest    |
|     2      |   schubb1    |
|     3      |   schubb2    |
+------------+--------------+


list_active_vols.py
	This script dumps out the information on the volumes on the cluster
-----------------------------------------------------------------------------------------------------------------------------------------		
c:\Git\element-test-branch>python list_active_vols.py -u admin -m solidfire-test
Enter password for user: admin on cluster solidfire-test:
Using token authentication
+-----------------------------+----+-----------+---------+----------------------+--------------+---------------------------------------------------------------+----------------------+----------------------+-----------+---------+---------+------------+----------------------------------+--------+-------------+---------+---------------+-------------+--------------------------------------+
| Name                        | ID | Access    | Account | Created              | Snapmirrored | IQN                                                           | Last Access          | Last IO              | Burst QoS | Max Qos | Min Qos | QoS Policy | NAA ID                           | Status | Size in GiB | VVol ID | Access Groups | Paired Vols | UUID                                 |
+-----------------------------+----+-----------+---------+----------------------+--------------+---------------------------------------------------------------+----------------------+----------------------+-----------+---------+---------+------------+----------------------------------+--------+-------------+---------+---------------+-------------+--------------------------------------+
| VSSTest001                  | 1  | readWrite | 1       | 2020-10-26T19:51:04Z | False        | iqn.2010-01.com.solidfire:p1gn.vsstest001.1                   | 2021-03-01T15:30:55Z | 2021-02-28T13:35:00Z | 15000     | 15000   | 50      | None       | 6f47acc1000000007031676e00000001 | active | 93.13       | None    | [1]           | []          | 930338fd-d61a-48c9-99b8-f4632fe04474 |
| VSSTest002                  | 2  | readWrite | 1       | 2020-10-26T19:51:28Z | False        | iqn.2010-01.com.solidfire:p1gn.vsstest002.2                   | 2021-03-01T15:00:52Z | 2021-02-28T13:35:00Z | 15000     | 15000   | 50      | None       | 6f47acc1000000007031676e00000002 | active | 111.76      | None    | [1]           | []          | 3730c2f4-2d51-494e-b282-519cf053e7f5 |
| VSSTest003                  | 3  | readWrite | 1       | 2020-10-26T19:52:09Z | False        | iqn.2010-01.com.solidfire:p1gn.vsstest003.3                   | 2021-03-01T15:30:55Z | 2021-02-28T13:35:00Z | 15000     | 15000   | 50      | None       | 6f47acc1000000007031676e00000003 | active | 139.7       | None    | [1]           | []          | 8fd7b26c-a21e-49cd-ae31-00176356ac59 |
| RCL-SQLTest-snap23-c7b001b3 | 13 | readWrite | 1       | 2020-10-27T16:12:22Z | False        | iqn.2010-01.com.solidfire:p1gn.rcl-sqltest-snap23-c7b001b3.13 | 2021-03-01T15:00:55Z | 2020-10-27T23:37:23Z | 15000     | 15000   | 50      | None       | 6f47acc1000000007031676e0000000d | active | 93.13       | None    | [1]           | []          | ec75053e-b218-4ce6-9962-237bacd1f0d3 |
| RCL-SQLTest-snap25-c7b001b3 | 14 | readWrite | 1       | 2020-10-27T16:12:22Z | False        | iqn.2010-01.com.solidfire:p1gn.rcl-sqltest-snap25-c7b001b3.14 | 2021-03-01T15:30:52Z | 2020-10-27T23:37:23Z | 15000     | 15000   | 50      | None       | 6f47acc1000000007031676e0000000e | active | 111.76      | None    | [1]           | []          | 74bf35c0-ff0f-459b-a878-f87c6486b5c5 |
| RCL-SQLTest-snap24-c7b001b3 | 15 | readWrite | 1       | 2020-10-27T16:12:22Z | False        | iqn.2010-01.com.solidfire:p1gn.rcl-sqltest-snap24-c7b001b3.15 | 2021-03-01T15:30:52Z | 2020-12-18T12:31:57Z | 15000     | 15000   | 50      | None       | 6f47acc1000000007031676e0000000f | active | 139.7       | None    | [1]           | []          | cb7881de-d81d-4b43-bbcc-16df2c5714b7 |
| schubb-test1                | 51 | readWrite | 2       | 2021-03-02T16:37:09Z | False        | iqn.2010-01.com.solidfire:p1gn.schubb-test1.51                | None                 | None                 | 15000     | 15000   | 50      | None       | 6f47acc1000000007031676e00000033 | active | 0.93        | None    | []            | []          | 58da6131-6aa1-48cf-9b33-82eb509906a6 |
| schubb-test1a               | 52 | readWrite | 2       | 2021-03-02T16:37:26Z | False        | iqn.2010-01.com.solidfire:p1gn.schubb-test1a.52               | None                 | None                 | 15000     | 15000   | 50      | None       | 6f47acc1000000007031676e00000034 | active | 0.93        | None    | []            | []          | e9aa7dde-7cc2-40f8-905a-8af7822dd02e |
| schubb-test2                | 53 | readWrite | 3       | 2021-03-02T16:37:57Z | False        | iqn.2010-01.com.solidfire:p1gn.schubb-test2.53                | None                 | None                 | 15000     | 15000   | 50      | None       | 6f47acc1000000007031676e00000035 | active | 0.93        | None    | []            | []          | 42fe7571-759a-41b0-ac1f-d7f3e420029b |
+-----------------------------+----+-----------+---------+----------------------+--------------+---------------------------------------------------------------+----------------------+----------------------+-----------+---------+---------+------------+----------------------------------+--------+-------------+---------+---------------+-------------+--------------------------------------+


list_replicated_vols.py
	This script lists the replicated volumes on a given cluster
	working on finding a replicating cluster to display output
-----------------------------------------------------------------------------------------------------------------------------------------
c:\Git\element-test-branch>python list_replicated_vols.py -u admin -m solidfire-test
Enter password for user admin on cluster solidfire-test:
Using token authentication
No replication found

output should resemble the following as the script was intended to verify that only a single replication existed for a cluster and volume
Volume -
        Passed:
        Total number of replication destinations is: {1}
Cluster -
        +-----------------+--------------------+
        | Cluster Pair ID |    Cluster Name    |
        +-----------------+--------------------+
        |        1        |  SOLIDFIRE-TEST-2  |
        +-----------------+--------------------+
        Passed: only one replication target


list_virt_nets.py
	This script lists out the configured VLANs
-----------------------------------------------------------------------------------------------------------------------------------------
c:\Users\cscott\OneDrive - NetApp Inc\Documents\scripts\python\sf>python list_virt_nets.py -u admin -m solidfire-test
Enter password for user admin on cluster solidfire-test:
Using token authentication
+---------+----------+----------+----------------------+-----------+---------------+---------+------+-----------+
| VLAN ID | Name     | VLAN Tag | Description          | SVIP      | Netmask       | Gateway | Size | Available |
+---------+----------+----------+----------------------+-----------+---------------+---------+------+-----------+
| 1       | ESX1122  | 1122     | VLAN for ESX hosts   | 1.1.1.254 | 255.255.255.0 | 0.0.0.0 | 4    | 0000      |
| 2       | ESX_2233 | 2233     | No description found | 2.2.2.254 | 255.255.255.0 | 0.0.0.0 | 4    | 0000      |
| 4       | ESX_2233 | 1121     | testylan             | 2.1.1.3   | 255.255.255.0 | 0.0.0.0 | 4    | 0000      |
+---------+----------+----------+----------------------+-----------+---------------+---------+------+-----------+


lldp2.py
	This script is a base implementation of the LLDP protocol's output
	LLDP is used to gather switch information
-----------------------------------------------------------------------------------------------------------------------------------------
repl_lag.py
	This script was put together to show how to pull replication information
		It was necessary as the information is stored with the volume, not the replication information
-----------------------------------------------------------------------------------------------------------------------------------------
set_qos_policy.py
	This script allows you to implement QoS policies across a cluster
	It will alert you if there are mismatches without --force-reset
-----------------------------------------------------------------------------------------------------------------------------------------