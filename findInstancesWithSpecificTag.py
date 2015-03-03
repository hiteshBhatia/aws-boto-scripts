import boto.ec2
import sys

ec2conn = boto.ec2.connect_to_region('ap-southeast-1')

reservations = ec2conn.get_all_instances(filters=({'tag-key':'Env','tag-value':'Replica'}))

for reservation in reservations:
    for instance in reservation.instances:
        print instance.image_id + " " + str(instance.tags)



