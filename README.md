# ec2_snapshot_retention-scripts

A collection of real-world Python automation scripts using `boto3` to manage AWS infrastructure.

Projects:

EC2 Snapshot Backup
- `ec2_snapshot_backup.py`: Automates volume snapshot creation
- `delete_old_snapshots.py`: Deletes snapshots older than 7 days

 SSM Remote Command Execution
- `ssm_command_test.py`: Executes shell commands on EC2 via AWS SSM

Tech Used
- Python 3.11
- boto3
- AWS EC2, SSM, EBS

To Run
```bash
pip install boto3
python script_name.py
