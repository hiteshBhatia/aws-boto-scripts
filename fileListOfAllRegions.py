import boto.ec2

regions = boto.ec2.regions()

print regions
print dir(regions.count)


for region in regions:
    print region.name
