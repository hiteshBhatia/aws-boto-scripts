'''
README
@Vikash

This script will create snapshots of all the volumes and then tag those volumes with respect to their Instance Name.

This will also send notification Email using SNS to the subscribed list whether the script is executed successfully or not.

'''
import boto 
import sys
import datetime
from boto import ec2

connection=ec2.connect_to_region('us-east-1',aws_access_key_id='AKIAIVYTBJOM46TLPWLQ',aws_secret_access_key='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')

try:

	volumes=connection.get_all_volumes()

	def tag_volume(vol):
		instance_id=vol.attach_data.instance_id
		instance_tag=connection.get_all_tags({'resource-id':instance_id})
		for tag in instance_tag:
			vol.add_tag('Name',tag.value)

	for volume in volumes:
		connection.create_snapshot(volume.id,tag_volume(volume))	


	print 'Script Executed Successfully'
except :
    print 'Some Error occurred : '
    print sys.exc_info()


