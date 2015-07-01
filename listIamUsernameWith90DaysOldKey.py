# This script will result all the AWS IAM Users whose access keys are 90 days old

import datetime
import dateutil
from dateutil import parser

import boto
from boto import iam


conn=iam.connect_to_region('ap-southeast-1')
users=conn.get_all_users()
timeLimit=datetime.datetime.now() - datetime.timedelta(days=90)

print "---------------------------------------------"
print "Access Keys Date" + "\t\t" + "Username"
print "---------------------------------------------"


for user in users.list_users_response.users:

    accessKeys=conn.get_all_access_keys(user_name=user['user_name'])

   for keysCreatedDate in accessKeys.list_access_keys_response.list_access_keys_result.access_key_metadata:

        if parser.parse(keysCreatedDate['create_date']).date() <= timeLimit.date():
          
            print(keysCreatedDate['create_date']) + "\t\t" + user['user_name']

