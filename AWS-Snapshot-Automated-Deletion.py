import boto3  # Module to use the AWS services like EC2 and S3
import re  # Module to check if a particular string matches
import datetime # Module to supplies classes for manipulating dates and times in both simple and complex ways

#Please mention your region name
#below line code is call cross region
ec = boto3.client('ec2', region_name='ap-southeast-2')  
iam = boto3.client('iam')

#begins lambda function
def lambda_handler(event, context):  
    account_ids = list()
    try:         
        iam.get_user()
    except Exception as e:
        # use the exception message to get the account ID the function executes under
        account_ids.append(re.search(r'(arn:aws:sts::)([0-9]+)', str(e)).groups()[1])

    delete_on = datetime.date.today().strftime('%Y-%m-%d')
    filters = [
        {'Name': 'tag-key', 'Values': ['DeleteOn']},
        {'Name': 'tag-value', 'Values': [delete_on]},
    ]
    snapshot_response = ec.describe_snapshots(OwnerIds=account_ids, Filters=filters)

    for snap in snapshot_response['Snapshots']:
        print "Deleting snapshot %s" % snap['SnapshotId']
        ec.delete_snapshot(SnapshotId=snap['SnapshotId'])