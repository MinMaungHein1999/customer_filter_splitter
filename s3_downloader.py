from file_manager import FileManager
import boto3
import zipfile
import os
import logging
logging.basicConfig(level=logging.INFO)

class S3Downloader:

    def __init__(self, bucket, region_name, temp_path):
        self.bucket = bucket
        self.s3_client = boto3.client('s3')
        self.temp_path = temp_path
        self.region_name = region_name

    def download_file_from_s3(self):

        s3 = self.s3_client

        if os.path.exists(self.temp_path):
            file_manager = FileManager(self.temp_path, self.region_name)
            # file_manager.delete_files()
        else:
            print(f"Directory '{self.temp_path}' is exist. Skipping file deletion operation.")


        response = s3.list_objects_v2(Bucket=self.bucket, Prefix='', Delimiter='/')

        file_contents = response.get('Contents', [])[:1]
        print(f'Listed files: {len(file_contents)}')

        gzip_files = [file_object for file_object in file_contents if file_object.get('Key', '').endswith('.zip')]

        self.extract_file_from_s3(gzip_files)

        return gzip_files

    def extract_file_from_s3(self, gzip_files):
        s3 = self.s3_client
        bucket = self.bucket
        
        temp_dir = self.temp_path
        os.makedirs(temp_dir, exist_ok=True)
        for file_object in gzip_files:
            file_name = os.path.basename(file_object['Key'])
            print(f'File name is {file_name}.')
            
            key = f'{file_name}'
            gzipped_file_path = os.path.join(temp_dir, file_name) 
            
            s3.download_file(bucket, key, gzipped_file_path)

            with zipfile.ZipFile(gzipped_file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)