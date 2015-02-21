import boto
from boto import iam

connection=iam.IAMConnection()

iamProfiles=connection.get_all_users();

for user in iamProfiles.users:

    mfaDevices = connection.get_all_mfa_devices(user.user_name)

    if mfaDevices.mfa_devices:
        print "User --->",user.user_name , " MFA : Enabled"
    else:
        print "User ---> ",user.user_name , "MFA : Disabled"



