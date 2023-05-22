# Ubuntu: Build Redisearch v2 module for Redis from source code

    Here is a tutorial to compile the Redisearch module v2.x for Redis by yourself. At the moment you can get it as binary only as subscriber of the Enterprise Version. With "apt-get" you can only install the Redisearch module v1.x. Version v1.x works fine, but has much less features. Without the subscription you can only build the v2.x version from the source code. The official documentation for the RediSearch module can be found here.

    RediSearch is the search engine or more precisely, the search index for the Redis database. It is currently the fastest search index you can install for free.

## Preparation, prerequisites for compiling

    Tested under Ubuntu 22.04
    All commands are executed under the Linux bash and as user "frank" and not directly as root! The hostname of the system is: "nexus". If "root" is needed, I use "sudo" for it.
    The home directory ~/redis is used for the source code and compilation
    All tools and programs needed for development under Ubuntu 22.04 must be installed before:

## Install dependencies packages

    sudo apt update 
    sudo apt install build-essential g++ make git

## Load source code via Git

    mkdir ~/redis 
    cd ~/redis 
    git clone --recursive https://github.com/RediSearch/RediSearch.git
    cd RediSearch


Tip: The "--recursive" is used to load submodules.
If you want to load a specific release via Git you can control this with the "--branch" option. For example, if we want to load the Redisearch release 2.4.15:

    git clone --recursive https://github.com/RediSearch/RediSearch.git --branch v2.4.15

This has the advantage that the correct version number of Redisearch also appears in the Redis log and in "redis-cli". Without the "--branch" specification a 99.99.99 (Git=master-xxx) appears as version.

## Check and install dependencies

Here the user password is requested (because internally "sudo" is called)

    make setup

## Build and linking

    make build

A sequence from 1% to 100% appears with a few "deprecated:" warnings. These can be ignored.

## Install Redis server and stop rediser server

make run 

## Load RediSearch module automatically when starting Redis

The newly created RediSearch module is located after the creation under:

    bin/linux-x64-release/search/redisearch.so

We now create a module directory under "/var/lib/redis/" and copy the newly created library "redisearch.so" into the created directory:

    sudo mkdir /var/lib/redis/modules
    sudo cp /bin/linux-x64-release/search/redisearch.so /var/lib/redis/modules/.

You can check the copy process with:

    sudo ls -la /var/lib/redis/modules/

The module should now appear under "/var/lib/redis/modules/".

Now we adjust the Redis server configuration file (/etc/redis/redis.conf). To do this, we open the file and add to it in the MODULES section:
    
    sudo nano /etc/redis/redis.conf

Tip: If you don't know how to use the "vi", you can replace it with the command "nano". So "sudo nano /etc/redis/redis.conf".

    ################################## MODULES #####################################

    # Load modules at startup. If the server is not able to load modules
    # it will abort. It is possible to use multiple loadmodule directives.
    #
    # loadmodule /path/to/my_module.so
    # loadmodule /path/to/other_module.so

    loadmodule /var/lib/redis/modules/redisearch.so

    ################################## NETWORK #####################################

Save the "redis.conf" file.

**Tip: You can copy the Redis library "redisearch.so" wherever you want. You just have to change the path under "loadmodule".**

## Restart Redis server:

    service redis-server start

With "status" you can test the Redis server and see if everything is running. Status: "Ready to accept connections" should appear.

In the logfile "/var/log/redis/redis-server.log" should appear the entry: "Module 'search' loaded from /var/lib/redis/modules/redisearch.so".

## Test Redis and RediSearch module in operation

The Redis server should now be running, the RediSearch module created, copied and activated. Now we test this at runtime using the "redis-cli":

    redis-cli
    127.0.0.1:6379> 

    127.0.0.1:6379> info modules
    # Modules
    module:name=search,ver=999999,api=1,filters=0,usedby=,using=,options=

    # search_version
    search_RedisSearch_version:7.0.5

    # search_index
    search_number_of_indexes:0

    # search_fields_statistics

    # search_runtime_configurations
    search_concurrent_mode:OFF
    search_enableGC:ON
    search_minimal_term_prefix:2
    search_maximal_prefix_expansions:200
    search_query_timeout_ms:500
    search_timeout_policy:return
    search_cursor_read_size:1000
    search_cursor_max_idle_time:300000
    search_max_doc_table_size:1000000
    search_max_search_results:1000000
    search_max_aggregate_results:-1
    search_search_pool_size:20
    search_index_pool_size:8
    search_gc_scan_size:100
    search_min_phonetic_term_length:3
    127.0.0.1:6379> 

If this appears, you have done everything right! Congratulations face-smile
