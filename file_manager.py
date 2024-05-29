import os
import csv
import shutil
import pandas as panda
from typing import List
from pn2_customer_factory import Pn2CustomerFactory
from pn2_customer import Pn2Customer
from vehicle_info import VehicleInfo
import tempfile
import logging
logging.basicConfig(level=logging.INFO)
import boto3
class FileManager:
    def __init__(self, excel_file_path, file_name,region_name, table_name, bucket):
        self.excel_file_path = excel_file_path
        self.file_name = file_name
        self.table_name = table_name
        self.region_name = region_name
        self.bucket = bucket
        self.s3_client = boto3.client('s3')

    def move_files_to_Dynamodb(self):
        self.file_to_save_db()
     
    def file_to_save_db(self):
        print(f"Start reading the excel file: '{self.excel_file_path}'")

        # Parse S3 path
        bucket, key = self._parse_s3_path(self.excel_file_path)

        # Download file from S3 to temporary location
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            self.s3_client.download_fileobj(bucket, key, temp_file)
            temp_file_path = temp_file.name

        try:
            with open(temp_file_path, mode='r', encoding='shift_jis_2004', newline='') as file:
                csv_reader = csv.reader(file)
                customer_array = []
                for row in csv_reader:
                    customer_array.append(self.row_to_customer(row).to_dict())

                customer_count = len(customer_array)
                print(f"Num of Customers in file ('{self.excel_file_path}'): '{customer_count}'")

                self.pn2_customer_factory = Pn2CustomerFactory(self.table_name, self.region_name, customer_array, self.bucket, self.file_name)
                self.pn2_customer_factory.create_customer()
        finally:
            os.remove(temp_file_path)

    def _parse_s3_path(self, s3_path):
        if s3_path.startswith("s3://"):
            s3_path = s3_path[5:]
        bucket, key = s3_path.split('/', 1)
        return bucket, key


    def row_to_customer(self, row):
        policy_number = row[0]
        branch_number = row[1]
        name_katakana = row[2]
        phone_number1 = row[4]
        number_plate6 = row[5]
        policy_term_effective_date = row[12]
        policy_term_end_date = row[13]
        number_plate1 = row[14]
        number_plate2 = row[15]
        number_plate3 = row[16]
        number_plate4 = row[17]
        number_plate5 = row[18]
        address_kanji = row[24]
        name_kanji = row[25]
        vehicle_name = row[26]

        vehicle_info = VehicleInfo( number_plate1, number_plate2, number_plate3, number_plate4, number_plate5, number_plate6, vehicle_name)
        
        customer = Pn2Customer(policy_number, branch_number, name_katakana, name_kanji, phone_number1, address_kanji, policy_term_effective_date, policy_term_end_date, vehicle_info)
        
        return customer