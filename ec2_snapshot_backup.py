import boto3
import datetime

# Set up EC2 client
ec2 = boto3.client('ec2', region_name='us-east-2')

# Get current date for tagging
timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')

# Step 1: Describe all running instances
instances = ec2.describe_instances(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
)

# Step 2: Loop through instances
for reservation in instances['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        print(f"\n📦 Backing up instance: {instance_id}")

        # Step 3: For each block device (EBS volumes)
        for device in instance.get('BlockDeviceMappings', []):
            volume_id = device['Ebs']['VolumeId']
            print(f"   → Creating snapshot of volume: {volume_id}")

            # Step 4: Create the snapshot
            ec2.create_snapshot(
    VolumeId=vol_id,
    Description=f"Auto backup {timestamp}",
    TagSpecifications=[
        {
            'ResourceType': 'snapshot',
            'Tags': [
                {'Key': 'CreatedBy', 'Value': 'AutoBackupScript'}
            ]
        }
    ]
)
            snapshot_id = snapshot['SnapshotId']

            # Step 5: Add tags
            ec2.create_tags(
                Resources=[snapshot_id],
                Tags=[
                    {'Key': 'Name', 'Value': f'Backup-{instance_id}'},
                    {'Key': 'InstanceId', 'Value': instance_id},
                    {'Key': 'VolumeId', 'Value': volume_id},
                    {'Key': 'Timestamp', 'Value': timestamp}
                ]
            )

            print(f"   ✅ Snapshot created: {snapshot_id}")
