'''
README
@Vikash


This script will find the Security Group having (0-65535) port open as well as port 22

'''


import sys
import boto 
from boto import ec2
from boto import sns
connection=ec2.connect_to_region("region-name")
connSNS = boto.sns.connect_to_region("region-name")
sg=connection.get_all_security_groups()

listOfInstances=""
messages="Following Instances have port 22 open"
def getTag(instanceId):

	reservations=connection.get_all_instances(filters={'instance_id':instanceId})
	for r in reservations:
		for i in r.instances:
			return i.tags['Name']

try:

	for securityGroup in sg:
	   for rule in securityGroup.rules:

		
		   global instanceId;
	
		   if (rule.from_port=='0' and rule.to_port == '65535')  and '0.0.0.0/0' in str(rule.grants):
			   for instanceid in securityGroup.instances():
			   	 instanceId=str(instanceid)		       		       		       
				 print "All ports open:"
				 print " SecurityGroupName: %s --> Instance Name: %s" %(securityGroup.name,  getTag(instanceId.split(':')[1]))
				 print "--------------------------------------------------------------------"
 	          
      		   if (rule.from_port=='22' and rule.to_port == '22')  and '0.0.0.0/0' in str(rule.grants):
                           for instanceid in securityGroup.instances():
		
                                 instanceId=str(instanceid)
				 listOfInstances += "Instance Name : " + getTag(instanceId.split(':')[1]) + "\t State:" + instanceid.state +"\n"
                                 print "Port 22 open for all IP:"
             			 print " SecurityGroupName: %s --> Instance Name: %s" %(securityGroup.name,  getTag(instanceId.split(':')[1]))
				 print " Instance State : %s " %(instanceid.state)
				 print  "-------------------------------------------------------------------"
	
				 connSNS.publish(topic='sns-arn-endpoint',message = messages + "\n" +  listOfInstances, subject='ProjectName : Server List with Port 22 Open')
	
except :
    print 'Some Error occurred : '
    print sys.exc_info()
    connSNS.publish(topic='sns-arn-endpoint',message = sys.exc_info(), subject='script ended with error')
#     
#     
