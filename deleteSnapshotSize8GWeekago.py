import boto 
import datetime
import dateutil
from dateutil import parser
from boto import ec2


connection=ec2.connect_to_region("ap-southeast-1")


snapshotsID=connection.get_all_snapshots(filters={'owner-id':611762388050,'volume-size':8})



timeLimit=datetime.datetime.now() - datetime.timedelta(days=7)


count=0

for sID in snapshotsID:
 if parser.parse(sID.start_time).date() < timeLimit.date():

	if "Created by CreateImage" in sID.description:
		print "Do thing"
	else:

		print "Deleting Snapshot %s " %(sID.id)	
        	connection.delete_snapshot(sID.id)




