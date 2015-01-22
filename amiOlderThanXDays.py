import boto.ec2
from datetime import date, timedelta,datetime
from dateutil.parser import parse
import csv

days_counter=45
region="ap-southeast-1"
class Ami:
    def  __init__(self,ec2_ami):
        self.id = ec2_ami.id
        self.strpdate = parse(ec2_ami.creationDate).date()



## Computing Older date 
old  = datetime.today() - timedelta(days_counter)
old_date=old.date()

## Fetching All AMI's
ec2conn = boto.ec2.connect_to_region(region)
amis=ec2conn.get_all_images(owners='self')

print "Today's date : " + str(datetime.today())
print "Finding AMI's older than : " + str(old_date)

older_list = []
for ami in amis:
    older_list = [ami for ami in amis if parse(ami.creationDate).date() < old_date ]



for item in older_list:
    print item.id + "," + item.name + "," + item.creationDate

print "Total : " + str(len(older_list))
