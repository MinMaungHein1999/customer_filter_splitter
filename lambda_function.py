import json
import os
from pn2_customer_import_to_dynamodb import Pn2CustomerImportToDynamodb
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    print("event", event)
  
    bucket_name = os.environ['BUCKET']
    table_name = os.environ['PN2_CUST_DATA_TABLE']
    region_name = os.environ['REGION_NAME']

    # request body
    body = event['body']
    csv_file_path = body['csv_file_path']
    file_name = body['file_name']
    
    try:
        pn2_cust_import_to_dynamodb = Pn2CustomerImportToDynamodb(csv_file_path, file_name, table_name, region_name, bucket_name)
        pn2_cust_import_to_dynamodb.call()
    
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully imported PN2 Customer Data from S3 into DynamoDb')
        }
            
    except ClientError as e:
        
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error occurred while importing : {e}')
        }
 
  
    
