import boto.ec2
import sys

regions = boto.ec2.regions()

for region in regions:
    try:
        ec2conn = boto.ec2.connect_to_region(region.name);
        reservations = ec2conn.get_all_reservations();

        for reservation in reservations:
                for instance in reservation.instances:
                    print instance.image_id + " " + str(instance.tags)

    except:
        print(sys.exc_info());


