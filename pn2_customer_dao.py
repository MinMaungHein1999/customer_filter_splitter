from botocore.exceptions import ClientError
import boto3
from dynamo_db_manager import DynamoDbManager
from s3_file_creator import S3FileCreator
import time
class Pn2CustomerDao:
    def __init__(self, table_name, region_name, customer_array, bucket, file_name):
        self.file_name = file_name
        self.table_name = table_name
        self.customer_array = customer_array
        self.region_name = region_name
        self.bucket = bucket
        self.prefix_name = "customer_data"
      
    def save_customer_to_dynamodb(self):
        print(f'Writing the data into {self.table_name}...')
        batch_size = 10000
        total_customers = len(self.customer_array)
        for i in range(0, total_customers, batch_size):
            batch_name = f"{i // batch_size + 1}_of_{total_customers // batch_size + 1}"
            try:
                batch_items = self.customer_array[i:i + batch_size]
                s3_file_creator = S3FileCreator( self.bucket, batch_items, self.file_name, batch_name)
                s3_file_creator.create_file()
            except ClientError as e:
                error_code = e.response['Error']['Code']
                error_message = e.response['Error']['Message']
                print(f"Error ({error_code}): {error_message}")
            print(f"Processed batch {batch_name}")
            time.sleep(3)