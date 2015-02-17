import boto.ec2

regions = boto.ec2.regions()
count = 0

#ec2conn = boto.ec2.connect_to_region('ap-southeast-1')
for region in regions:
    try:
        ec2conn = boto.ec2.connect_to_region(region.name)
        ips =  ec2conn.get_all_addresses()

        for ip in ips:
            unattached_volumes = [ volume for volume in vols if volume.attachment_state() ==  None ]
            count = count + len(unattached_volumes)
            print "Total of " + str(len(unattached_volumes)) + " unattached volumes in regions " + str(region.name)
    except:
        print "No Access To Region : " + region.name

print "Total " + str(count) + " unattached Volumes"




