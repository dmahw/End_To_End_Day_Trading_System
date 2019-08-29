End 2 End Day Trading System Python
===================================

## Requirements
* Ubuntu 18.04
* Python 3.6.7
* PyMongo 3.9.0
* MongoDB 4
* HAProxy (Optional: Only for multiple transaction servers)

## Description

This day trading system was develop as a final course project to understand the concept and fundamentals of distributed systems. 

Quotes are all simulated and have the option to connect to another server to receive quotes from an external source, otherwise quotes are set at a fixed amount. All quotes are stored in a cache to provide better performance, and expire after 60 seconds to ensure quotes are updated. 

Every user transaction creates a new thread in a transaction server, and is handled seperately from other user transactions. A user is not limited to 1 server, and can be handled by any transaction server as they all access the same database.

All performance numbers mentioned in the presentation are dependant on the performance of the systems utilized for testing.

The workload generator reads the entire workload file before sending any transactions, and creates a thread per unique user. To simulate more than 300 unique users, multiple workload generators must be used as one workload generator is limited to 300 unique users.

## Instructions

1. Install all necessary requirements
2. Start the MongoDB database service
3. Inside the transactionServer folder, run 
  * `python server.py _hostIP_ _hostPort_ _databaseIP_ _databasePort_`
  
4. For multiple transaction servers, run the same command as above but with different _serverIP_ and _serverPort_ values. This will require a load balancer, we used HAProxy. An example configuration file can be found in _haproxyConfix.txt_

5. Inside the workloadGenerator folder, run
  * `python clients.py _workloadFile_ _serverIP_ _serverPort_`
  * Please see the workload generator section for the workload files

## Quotes
* All quotes are simulated
* Quotes are stored in a cache 
* Quotes expire after 60 seconds
