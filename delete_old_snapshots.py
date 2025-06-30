import boto3
from datetime import datetime, timezone, timedelta

# Setup
ec2 = boto3.client('ec2', region_name='us-east-2')  # adjust if needed
days_to_keep = 7
delete_before = datetime.now(timezone.utc) - timedelta(days=days_to_keep)

# Optional filter: Only delete snapshots created by this backup script
snapshot_filter_tag_key = 'CreatedBy'
snapshot_filter_tag_value = 'AutoBackupScript'  # Make sure your backup script tags snapshots with this

# Get all snapshots owned by this account
snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']

deleted_count = 0

for snap in snapshots:
    start_time = snap['StartTime']
    snapshot_id = snap['SnapshotId']
    tags = {tag['Key']: tag['Value'] for tag in snap.get('Tags', [])}

    # Only delete snapshots made by your script
    if tags.get(snapshot_filter_tag_key) != snapshot_filter_tag_value:
        continue

    if start_time < delete_before:
        print(f"🗑️ Deleting old snapshot: {snapshot_id} (created on {start_time})")
        ec2.delete_snapshot(SnapshotId=snapshot_id)
        deleted_count += 1

print(f"\n✅ Done. Deleted {deleted_count} snapshot(s) older than {days_to_keep} days.")
