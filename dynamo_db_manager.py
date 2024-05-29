import boto3
from botocore.exceptions import ClientError
import time
class DynamoDbManager:
    @staticmethod
    def table_exists(table_name, region_name):
        dynamodb = boto3.client('dynamodb', region_name=region_name)
        try:
            dynamodb.describe_table(TableName=table_name)
            return True
        except dynamodb.exceptions.ResourceNotFoundException:
            return False
    
    @staticmethod
    def wait_for_table_deletion(table_name, region_name):
        dynamodb = boto3.client('dynamodb', region_name=region_name)
        while True:
            try:
                dynamodb.describe_table(TableName=table_name)
                print(f'Waiting for table {table_name} to be deleted...')
                time.sleep(5)
            except dynamodb.exceptions.ResourceNotFoundException:
                print(f'Table {table_name} has been successfully deleted.')
                break

    @staticmethod
    def wait_for_table_creation(table_name, region_name):
        dynamodb = boto3.client('dynamodb', region_name=region_name)
        while True:
            try:
                dynamodb.describe_table(TableName=table_name)
                print(f'Table {table_name} has been successfully created.')
                break
            except dynamodb.exceptions.ResourceNotFoundException:
                print(f'Waiting for table {table_name} to be crated...')
                time.sleep(5)
                
    
    @classmethod
    def create_table_if_not_exists(cls, table_name, key_schema, region_name, global_secondary_indexes, attribute_definitions):
        dynamodb = boto3.client('dynamodb', region_name=region_name)

        try:
            # Check if the table already exists
            if cls.table_exists(table_name, region_name):
                dynamodb.delete_table(TableName=table_name)
                cls.wait_for_table_deletion(table_name, region_name)
            
            # Create the table
            dynamodb.create_table(
                TableName=table_name,
                KeySchema=key_schema,
                AttributeDefinitions=attribute_definitions,
                GlobalSecondaryIndexes=global_secondary_indexes,
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            
            # Wait for the table to be created
            while not cls.table_exists(table_name, region_name):
                print(f'Waiting for table {table_name} to be created...')
                time.sleep(5)
            
            print(f'Table {table_name} has been successfully created.')
        
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print(f'Table {table_name} already exists.')
            else:
                print(f'Error creating table {table_name}: {e}')
