zookeeper-rpm
---------
A set of scripts to package zookeeper into an rpm

Setup
-----
    $ yum groupinstall "Development Tools"

Building
--------
    $ make rpm

Resulting RPM will be avaliable at $(shell pwd)/x86_64

Installing and operating
------------------------
    $ sudo yum install zookeeper*.rpm
    $ sudo service zookeeper start
    $ sudo chkconfig zookeeper on

Default locations
-----------------
libs, binaries and database: /opt/zookeeper  
logs: /var/log/zookeeper  
configs: /etc/zookeeper  
