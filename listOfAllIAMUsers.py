import boto
from boto import iam

connection=iam.IAMConnection()

iam_profiles=connection.get_all_users();
for user in iam_profiles.users:
    print user.user_name