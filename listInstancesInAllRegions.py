
#Find list of all the regions.
#Find list of all the  running instances.

import boto
from boto import ec2

region=ec2.regions()

for reg in region:

    connection=ec2.connect_to_region(reg.name)

    if reg.name == "us-gov-west-1" or reg.name == "cn-north-1":
        print "API call is not allowed in this regions:",".",reg.name
        continue

    reservation=connection.get_all_reservations()

    if reservation:
        print "Instances in ",'.',reg.name
        for r in reservation:
            for i in r.instances:
                print i.tags['Name'], i.ip_address
    else:
        print "No Instances in available in region: ", "--" , reg.name



