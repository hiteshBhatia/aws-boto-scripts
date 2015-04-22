import boto
import time
from boto import ec2
from datetime import date, timedelta,datetime

retentionTag = 'Frequency'  # Frequency is in number
searchTag = 'instance_id'
region = '<region>'
accountId = '<account-id>'
backupTag = "AutomaticBackup"
defaultFrequency = 1
count = 0


def getFrequencyCount(tags):
    print tags
    try:
        fq = tags[retentionTag];
    except:
        fq = defaultFrequency
    return fq

def getBackupAMIName(instance,imageCount):
    try:
        backupName = instance.tags["Name"]
    except:
        backupName = instance.id
    return str(backupName) + "-" + str(time.strftime("%Y-%m-%d"))
    # return str(backupName) + "-" + str(time.strftime("%Y-%m-%d")) + "-" + str(imageCount + 1)



connection = ec2.connect_to_region(region)
reservations = connection.get_all_reservations(filters={"instance-state-name": "running", "tag-key": backupTag, "tag-value": "True"})

currentDatestr=str(time.strftime("%Y-%m-%d")) + "*"

for reservation in reservations:
    for instance in reservation.instances:
        Frequency = getFrequencyCount(instance.tags)
        all_ami = connection.get_all_images(owners=accountId, filters={"tag-key": searchTag, "tag-value": instance.id,"creation-date":currentDatestr})


        print str(instance.id) + ": Found " + str(len(all_ami)) + " backups, required is " + str(Frequency)
        imageCount=len(all_ami)
        if (int(Frequency) > imageCount):
            backupName=getBackupAMIName(instance,imageCount)
            print "Creating AMI Named " + backupName
            createdImageId = connection.create_image(instance.id, name=backupName,no_reboot=True)
            image = connection.get_image(createdImageId)
            image.add_tag('instance_id', instance.id)