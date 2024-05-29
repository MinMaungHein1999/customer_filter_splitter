import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
import datetime
class S3FileCreator:
    def __init__(self, bucket, batch_tiems, file_name, batch_name):
        self.bucket = bucket
        self.batch_name = batch_name
        self.file_name = file_name
        self.json_arr_objs = json.dumps(batch_tiems, indent=4)
        self.generate_unique_file_name()

    def generate_unique_file_name(self):
        unique_file_name = f"{self.file_name}_{self.batch_name}.json"
        self.file_name = unique_file_name

    def create_file(self):
        key = f"splited_file/{self.file_name}"
        s3 = boto3.client('s3')
        
        try:
            s3.put_object(Bucket=self.bucket, Key=key, Body=self.json_arr_objs)
            print(f"File {key} uploaded to S3 bucket {self.bucket}.")
        except NoCredentialsError:
            print("Error: AWS credentials not found.")
        except PartialCredentialsError:
            print("Error: Incomplete AWS credentials provided.")
        except ClientError as e:
            print(f"Error: Failed to upload file to S3. {e.response['Error']['Message']}")

        print(f"File {self.file_name} uploaded to S3 bucket {self.bucket}.")