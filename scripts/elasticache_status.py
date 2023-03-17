#! /usr/bin/env python

import boto3
import time

session = boto3.Session(profile_name='default')
client = session.client('elasticache')

response = client.describe_replication_groups(
    ReplicationGroupId='qat-redisq'
)
start_time = time.time()

while True:
    now = time.strftime("%d/%b/%Y %H:%M:%S")
    current_iteration_time = time.time()
    elasped_time = current_iteration_time - start_time
    elasped_time_expanded = time.strftime("%H:%M:%S", time.gmtime(elasped_time))
    status = response['ReplicationGroups'][0]['Status']
    # print(f"{time.time} Status: {response['ReplicationGroups'][0]['Status']},sep='', end='\r'")
    print(" {0}\t Status: {1}\t Elapsed Time: {2}".format(now, status, elasped_time_expanded), sep='', end='\r')
    time.sleep(5)