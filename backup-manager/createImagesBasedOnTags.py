import sys
import boto
import time
from boto import ec2
from datetime import date, timedelta, datetime


retentionTag = 'Frequency'  # Frequency is in number
searchTag = 'instance_id'
region = '<region>'
accountId = '<accountId>'
backupTag = "AutomaticBackup"
defaultFrequency = 1
count = 0



def getFrequencyCount(tags):
    try:
        fq = tags[retentionTag];
    except:
        fq = defaultFrequency
    return fq


def getBackupAMIName(instance, imageCount):
    try:
        backupName = instance.tags["Name"]
    except:
        backupName = instance.id
    return str(backupName) + "-" + str(time.strftime("%Y-%m-%d"))


def createImageWithTag(instance_id, backupName):
    try:
        print "Creating AMI Named " + backupName
        createdImageId = connection.create_image(instance_id, name=backupName, no_reboot=True)
        image = connection.get_image(createdImageId)
    except:
        print sys.exc_info()



connection = ec2.connect_to_region(region)
reservations = connection.get_all_reservations(
    filters={"instance-state-name": "running", "tag-key": backupTag, "tag-value": "True"})

currentDatestr = str(datetime.utcnow().strftime("%Y-%m-%d")) + "*"
print currentDatestr

for reservation in reservations:
    for instance in reservation.instances:
        print "-------------------------------------------------------------------"
        print str(instance) + " : " + str(instance.tags)

        Frequency = getFrequencyCount(instance.tags)
        all_ami = connection.get_all_images(owners=accountId, filters={"tag-key": searchTag, "tag-value": instance.id,"creation-date": currentDatestr})

        print str(instance.id) + ": Found " + str(len(all_ami)) + " backups, required is " + str(Frequency)

        imageCount = len(all_ami)
        if (int(Frequency) > imageCount):
            backupName=getBackupAMIName(instance,imageCount)
            createImageWithTag(instance.id,backupName)