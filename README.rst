easytwo
#######

Easy EC2 Queries.

Install
-------

::

    pip install easytwo

Usage
-----

::

    Usage: easytwo [OPTIONS]

      Easy EC2 Queries.

    Options:
      --id TEXT
      --name NAME
      --az AZ
      --state STATE
      --type TYPE
      --vpc VPC
      --ami AMI
      --public-ip PUBLIC-IP
      --private-ip PRIVATE-IP
      --tag TAG VALUE
      --output [id|az|state|type|public-ip|private-ip|ami|vpc|subnet]
      --help

Examples
--------

::

    easytwo --name mesos-master
    i-127ffc4eb5e9d6cab
    i-d5baaf2fd0e31c86e
    i-ed2faccb4d035b16a

::

    easytwo --name "es-*-cluster" --output id --output state --output private-ip
    i-7ba0fbae64d58c1f9 running 10.0.0.4
    i-af9cb4acf2e57d3d0 running 10.0.1.8
    i-ed316aecb5fb2809d running 10.0.2.15
    i-fe9b5acc2fb40d1a7 stopped 10.0.1.16


::

    easytwo --name mesos --tag NodeType Master --az us-east-1d --output type
    c4.large
    c4.large
    c4.large
