__author__ = 'Hitesh,Aakash'

import boto
import time
from datetime import date, timedelta,datetime
from dateutil.parser import parse
from boto import ec2

retentionTag = 'RetentionCount' ## Retention Count is in Days
searchTag='instance_id'
region = '<region>'
accountId = '<accountID>'
backupTag="AutomaticBackup"
defaultRetentionCount=30


def getRetentionCountFromTags(tags):
    print tags
    try:
        rc = tags[retentionTag];
    except:
        rc = defaultRetentionCount
    return rc

def getRetentionDate(retentionCount):
    checkpoint  = datetime.today() - timedelta(int(retentionCount))
    return checkpoint.date()


connection = ec2.connect_to_region(region)
reservations = connection.get_all_reservations(filters={"tag-key": backupTag, "tag-value": "True"})

for reservation in reservations:
    for instance in reservation.instances:

        retentionCount=getRetentionCountFromTags(instance.tags)
        retentionDate=getRetentionDate(retentionCount)

        print "Deleting AMI Older than " +  str(retentionDate)

        amiList=connection.get_all_images(owners=accountId,filters={"tag-key": searchTag, "tag-value": instance.id})
        amiList = sorted(amiList, key=lambda ami: ami.creationDate)

        for ami in amiList:
            if parse(ami.creationDate).date() < retentionDate:
                print "Deleting AMI ID " + str(ami.id) + " Created On " + str(ami.creationDate)
                blockDeviceMapping = ami.block_device_mapping
                connection.deregister_image(ami.id)
                for snapshot in blockDeviceMapping:
                        snapshotID=blockDeviceMapping[snapshot].snapshot_id
                        if snapshotID is not None:
                                print "-------------------------------------------------------------------------------------"
                                print "Deleting Snapshot " + str(snapshotID)
                                connection.delete_snapshot(snapshotID)
                                print "-------------------------------------------------------------------------------------"
		#connection.deregister_image(ami.id, delete_snapshot = True)
            else:
                print str(ami.id) + "has a creation date " + str(ami.creationDate) + " more recent than Deletion Date " + str(retentionDate)
                break;


